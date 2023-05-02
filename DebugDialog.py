from PySide6.QtCore import QSize, QTimer
from PySide6.QtWidgets import (
  QVBoxLayout, QDialog
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import numpy as np

class DebugDialog (QDialog):
  def __init__ (self, model, data_len, interval):
    super().__init__()
    self.model = model
    self.setWindowTitle('debug')
    self.resize(QSize(1000, 600))
    self.fig, self.ax = plt.subplots()
    self.data = np.zeros((self.model.NUM_OF_VALUES, data_len))
    for i in range(self.model.NUM_OF_VALUES):
      self.ax.plot(np.arange(0, data_len), self.data[i])
    self.data_len = data_len
    canvas = FigureCanvas(self.fig)
    layout = QVBoxLayout()
    layout.addWidget(canvas)
    self.setLayout(layout)
    self.ani = animation.FuncAnimation(self.fig, self.update, frames=None, interval=interval, blit=True, cache_frame_data=False)

  def update (self, frame):
    self.data[:, : -1] = self.data[:, 1: ]
    self.data[:, -1: ] = np.expand_dims(self.model.debug_values, axis=1) - 2000
    self.ax.cla()
    ret = []
    for data in self.data:
      ret += self.ax.plot(np.arange(0, self.data_len), data)
    return ret
