from PySide6.QtCore import QSize, QTimer
from PySide6.QtWidgets import (
  QVBoxLayout, QDialog
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import numpy as np
from matplotlib.ticker import AutoLocator, ScalarFormatter

class AngleDebugDialog (QDialog):
  def __init__ (self, model, data_len, interval):
    super().__init__()
    self.model = model
    self.setWindowTitle('debug')
    self.resize(QSize(1000, 600))
    self.fig, self.ax = plt.subplots()
    self.data = np.zeros((5, data_len))
    for i in range(5):
      self.ax.plot(np.arange(0, data_len), self.data[i])
    self.data_len = data_len
    canvas = FigureCanvas(self.fig)
    layout = QVBoxLayout()
    layout.addWidget(canvas)
    self.setLayout(layout)
    self.ani = animation.FuncAnimation(self.fig, self.update, frames=None, interval=interval, blit=True, cache_frame_data=False)
    self.closeEvent = self.handle_close

  def update (self, frame):
    self.data[:, : -1] = self.data[:, 1: ]
    self.data[:, -1: ] = np.expand_dims(self.model.debug_values[0: 5], axis=1) - 15000
    self.ax.cla()
    self.ax.set_ylim(-2000, 2000)
    ret = []
    for data in self.data:
      ret += self.ax.plot(np.arange(0, self.data_len), data)
    return ret

  def handle_close (self, event):
    self.ani.event_source.stop()
    self.fig.clf()
    plt.close(self.fig)
    event.accept()

class EscDebugDialog (QDialog):
  def __init__ (self, model, data_len, interval):
    super().__init__()
    self.model = model
    self.setWindowTitle('debug')
    self.resize(QSize(1000, 600))
    self.fig, self.ax = plt.subplots()
    self.data = np.zeros((4, data_len))
    for i in range(4):
      self.ax.plot(np.arange(0, data_len), self.data[i])
    self.data_len = data_len
    canvas = FigureCanvas(self.fig)
    layout = QVBoxLayout()
    layout.addWidget(canvas)
    self.setLayout(layout)
    self.ani = animation.FuncAnimation(self.fig, self.update, frames=None, interval=interval, blit=True, cache_frame_data=False)
    self.closeEvent = self.handle_close

  def update (self, frame):
    self.data[:, : -1] = self.data[:, 1: ]
    self.data[:, -1: ] = np.expand_dims(self.model.debug_values[5: 9], axis=1) - 15000
    self.ax.cla()
    self.ax.set_ylim(5250, 11000)
    ret = []
    for data in self.data:
      ret += self.ax.plot(np.arange(0, self.data_len), data)
    return ret
  
  def handle_close (self, event):
    self.ani.event_source.stop()
    self.fig.clf()
    plt.close(self.fig)
    event.accept()

class RawAngleDebugDialog (QDialog):
  def __init__ (self, model, data_len, interval):
    super().__init__()
    self.model = model
    self.setWindowTitle('debug')
    self.resize(QSize(1000, 600))
    self.fig, self.ax = plt.subplots()
    self.data = np.zeros((6, data_len))
    for i in range(6):
      self.ax.plot(np.arange(0, data_len), self.data[i])
    self.data_len = data_len
    canvas = FigureCanvas(self.fig)
    layout = QVBoxLayout()
    layout.addWidget(canvas)
    self.setLayout(layout)
    self.ani = animation.FuncAnimation(self.fig, self.update, frames=None, interval=interval, blit=True, cache_frame_data=False)
    self.closeEvent = self.handle_close

  def update (self, frame):
    self.data[:, : -1] = self.data[:, 1: ]
    self.data[:, -1: ] = np.expand_dims(self.model.debug_values[9: 15], axis=1) - 15000
    self.ax.cla()
    self.ax.set_ylim(-1000, 1000)
    ret = []
    for data in self.data:
      ret += self.ax.plot(np.arange(0, self.data_len), data)
    return ret

  def handle_close (self, event):
    self.ani.event_source.stop()
    self.fig.clf()
    plt.close(self.fig)
    event.accept()
