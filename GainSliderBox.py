from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
  QSlider, QWidget, QVBoxLayout,
  QLineEdit, QLabel
)
import math

class GainSliderBox (QWidget):
  def __init__ (self, label, slider, gain_idx, reservation):
    super().__init__()
    layout = QVBoxLayout(self)
    self.slider = slider
    self.line_edit = QLineEdit('0')
    self.line_edit.returnPressed.connect(self.handle_text_changed)
    layout.addWidget(QLabel(label))
    layout.addWidget(slider)
    layout.addWidget(self.line_edit)
    self.setLayout(layout)
    self.reservation = reservation
    self.gain_idx = gain_idx
    self.slider.valueChanged.connect(self.handle_slider_changed)
  
  def handle_text_changed (self):
    self.slider.setValue(math.floor(int(self.line_edit.text())))
    self.reservation.reserve(self.gain_idx, math.floor(int(self.line_edit.text())))
  
  def handle_slider_changed (self, pos):
    self.line_edit.setText(str(pos * self.slider.single_step))
    self.reservation.reserve(self.gain_idx, pos * self.slider.single_step)

class GainSlider (QSlider):
  def __init__ (self, min_max, single_step, *args, **kargs):
    super().__init__(*args, **kargs)
    self.setRange(min_max[0] // single_step, min_max[1] // single_step)
    self.setFixedSize(QSize(30, 300))
    self.single_step = single_step
  
  def get_value (self):
    return self.value * self.single_step
