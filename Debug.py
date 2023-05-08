import threading

class DebugThread:
  NUM_OF_VALUES = 15
  def __init__ (self, model, serial):
    self.ser = None
    self.port = None
    self.baud_rate = None
    self.payload_cnt = 0
    self.rx_buf = b''
    self.model = model
    self.serial = serial
    self.gain_crc = 0

  def process_serial_read (self):
    while True:
      if self.serial.ser != None and not self.serial.ser.closed:
        data = self.serial.ser.read(1)
        if self.payload_cnt == 0 and data == b'\x80':
          self.rx_buf = b''
          self.rx_buf += data
          self.payload_cnt += 1
        elif self.payload_cnt == 1 and data == b'\x81':
          self.rx_buf += data
          self.payload_cnt += 1
        elif self.payload_cnt >= 2 and self.payload_cnt < 2 + 2 * DebugThread.NUM_OF_VALUES:
          self.rx_buf += data
          self.payload_cnt += 1
        elif self.payload_cnt == 2 + 2 * DebugThread.NUM_OF_VALUES:
          self.gain_crc &= 0xff00;
          self.gain_crc |= int.from_bytes(data, 'little', signed=False);
          self.payload_cnt += 1
        elif self.payload_cnt == 2 + 2 * DebugThread.NUM_OF_VALUES + 1:
          check_sum = 0
          for i in range(0, (DebugThread.NUM_OF_VALUES + 1) * 2):
            check_sum += int.from_bytes(self.rx_buf[i: i + 1], 'little', signed=False)
          self.gain_crc &= 0x00ff
          self.gain_crc |= (int.from_bytes(data, 'little', signed=False) << 8)
          if 0xffff - check_sum == self.gain_crc:
            for i, j in zip(range(DebugThread.NUM_OF_VALUES), range(2, DebugThread.NUM_OF_VALUES * 2 + 2, 2)):
              self.model.debug_values[i] = int.from_bytes(self.rx_buf[j: j + 2], 'little', signed=False)
          self.payload_cnt = 0
        else:
          self.payload_cnt = 0

  def start (self):
    thread = threading.Thread(target=self.process_serial_read, daemon=True)
    thread.start()
