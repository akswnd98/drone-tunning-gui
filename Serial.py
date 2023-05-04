import serial

class SerialModel:
  def __init__ (self):
    self.ser = None
    self.is_connected = False

  def connect (self, port, baud_rate):
    self.ser = serial.Serial(port, baud_rate)
    self.is_connected = True
