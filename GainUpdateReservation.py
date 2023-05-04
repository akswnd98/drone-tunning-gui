import serial
import ctypes

class GainUpdateReservation:
  NUM_OF_GAINS = 10

  def __init__ (self, serial):
    self.is_changed = False
    self.gains = [0] * GainUpdateReservation.NUM_OF_GAINS
    self.is_connected = False
    self.serial = serial
  
  def reserve (self, gain_idx, pos):
    self.is_changed = True
    self.gains[gain_idx] = pos
  
  def update (self):
    if self.is_connected and self.is_changed:
      payload = (ctypes.c_uint16 * (GainUpdateReservation.NUM_OF_GAINS + 2))()
      payload[0] = 0x4020
      for i in range(1, GainUpdateReservation.NUM_OF_GAINS + 1):
        payload[i] = self.gains[i - 1]
      check_sum = 0
      for i in range (0, GainUpdateReservation.NUM_OF_GAINS + 1):
        check_sum += (payload[i] & 0x00ff) + ((payload[i] & 0xff00) >> 8)
      payload[GainUpdateReservation.NUM_OF_GAINS + 1] = 0xffff - check_sum
      self.serial.ser.write(bytes(payload))
      self.is_changed = False