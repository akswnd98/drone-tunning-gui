import threading
import serial

class DebugThread:
  NUM_OF_VALUES = 4
  def __init__ (self, model):
    self.ser = None
    self.port = None
    self.baud_rate = None
    self.payload_cnt = 0
    self.rx_buf = b''
    self.model = model

  def connect (self, port, baud_rate):
    self.port = port
    self.baud_rate = baud_rate
    self.ser = serial.Serial(self.port, self.baud_rate)

  def process_serial_read (self):
    while True:
      if self.ser != None and not self.ser.closed:
        data = self.ser.read(1)
        if self.payload_cnt == 0 and data == 0x20:
          self.rx_buf += data
          self.payload_cnt += 1
        elif self.payload_cnt == 1 and data == 0x40:
          self.rx_buf += data
          self.payload_cnt += 1
        elif self.payload_cnt >= 2 and self.payload_cnt < 2 + 2 * DebugThread.NUM_OF_VALUES:
          self.rx_buf += data
          self.payload_cnt += 1
        elif self.payload_cnt == 2 + 2 * DebugThread.NUM_OF_VALUES:
          gain_crc &= 0xff00;
          gain_crc |= data;
          self.payload_cnt += 1
        elif self.payload_cnt == 2 + 2 * DebugThread.NUM_OF_VALUES + 1:
          check_sum = 0
          for i in range(0, (DebugThread.NUM_OF_VALUES + 1) * 2):
            check_sum += self.rx_buf[i]
          crc &= 0x00ff
          crc |= (data << 8)
          if 0xffff - check_sum == crc:
            for i, j in zip(range(DebugThread.NUM_OF_VALUES), range(2, DebugThread.NUM_OF_VALUES * 2 + 2, 2)):
              self.model.debug_values[i] = int.from_bytes(self.rx_buf[j: j + 2], 'little')
            for i in range(DebugThread.NUM_OF_VALUES):
              print(self.model.debug_values[i], end=' ')
            print()
          self.payload_cnt = 0
        else:
          self.payload_cnt = 0

  def start (self):
    thread = threading.Thread(target=self.process_serial_read, daemon=True)
    thread.start()
