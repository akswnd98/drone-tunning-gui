import sys
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import (
  QApplication, QMainWindow, QWidget,
  QHBoxLayout, QMenuBar, QMenu
)
from PySide6.QtGui import QAction
from GainUpdateReservation import GainUpdateReservation
from GainSliderBox import GainSliderBox, GainSlider
from ConnectDialog import ConnectDialog
from DebugDialog import AngleDebugDialog, EscDebugDialog, RawAngleDebugDialog
from PDPannel import PDPannel
from Debug import DebugThread
from CurDebugValueModel import CurDebugValuesModel
from Serial import SerialModel

P_PHI_IDX = 0
D_PHI_IDX = 1
P_THETA_IDX = 2
D_THETA_IDX = 3
P_PHI_DOT_IDX = 4
D_PHI_DOT_IDX = 5
P_THETA_DOT_IDX = 6
D_THETA_DOT_IDX = 7
P_PSI_DOT_IDX = 8
D_PSI_DOT_IDX = 9

serial = SerialModel()

reservation = GainUpdateReservation(serial)
debug_values_model = CurDebugValuesModel()
debug_thread = DebugThread(debug_values_model, serial)

class MainWindow (QMainWindow):
  def __init__ (self) -> None:
    super().__init__()
    self.setWindowTitle('drone-tunning')
    self.setBaseSize(QSize(800, 400))
    self.setMenuBar(MenuBar())

class MainPannel (QWidget):
  def __init__ (self, widgets):
    super().__init__()
    layout = QHBoxLayout()
    for widget in widgets:
      layout.addWidget(widget)
    self.setLayout(layout)

class MenuBar (QMenuBar):
  def __init__ (self):
    super().__init__()
    self.addMenu(ConnectMenu())
    self.addMenu(DebugMenu())

class ConnectMenu (QMenu):
  def __init__ (self):
    super().__init__('connect')
    action = QAction('connect', self)
    action.triggered.connect(self.handle_triggered)
    self.addAction(action)
  
  def handle_triggered (self):
    dialog = ConnectDialog(serial)
    dialog.exec()

class DebugMenu (QMenu):
  def __init__ (self):
    super().__init__('debug')
    action = QAction('angle', self)
    action.triggered.connect(self.handle_angle_debug_triggered)
    self.addAction(action)
    action = QAction('esc', self)
    action.triggered.connect(self.handle_esc_debug_triggered)
    self.addAction(action)
    action = QAction('raw angle', self)
    action.triggered.connect(self.handle_raw_angle_debug_triggered)
    self.addAction(action)
  
  def handle_angle_debug_triggered (self):
    dialog = AngleDebugDialog(debug_values_model, 100, 1)
    dialog.show()
  
  def handle_esc_debug_triggered (self):
    dialog = EscDebugDialog(debug_values_model, 100, 1)
    dialog.show()
  
  def handle_raw_angle_debug_triggered (self):
    dialog = RawAngleDebugDialog(debug_values_model, 100, 1)
    dialog.show()

app = QApplication(sys.argv)

def get_update_gain (reservation):
  def update_gain ():
    reservation.update()
  return update_gain

timer = QTimer()
timer.setInterval(100)
timer.timeout.connect(get_update_gain(reservation))
timer.start()

window = MainWindow()
window.setCentralWidget(
  MainPannel([
    PDPannel(
      GainSliderBox('P_phi', GainSlider((0, 300), 1), P_PHI_IDX, reservation),
      GainSliderBox('D_phi', GainSlider((0, 300), 1), D_PHI_IDX, reservation)
    ),
    PDPannel(
      GainSliderBox('P_theta', GainSlider((0, 300), 1), P_THETA_IDX, reservation),
      GainSliderBox('D_theta', GainSlider((0, 300), 1), D_THETA_IDX, reservation)
    ),
    PDPannel(
      GainSliderBox('P_phi_dot', GainSlider((0, 300), 1), P_PHI_DOT_IDX, reservation),
      GainSliderBox('D_phi_dot', GainSlider((0, 300), 1), D_PHI_DOT_IDX, reservation)
    ),
    PDPannel(
      GainSliderBox('P_theta_dot', GainSlider((0, 300), 1), P_THETA_DOT_IDX, reservation),
      GainSliderBox('D_theta_dot', GainSlider((0, 300), 1), D_THETA_DOT_IDX, reservation)
    ),
    PDPannel(
      GainSliderBox('P_psi_dot', GainSlider((0, 1000), 1), P_PSI_DOT_IDX, reservation),
      GainSliderBox('D_psi_dot', GainSlider((0, 100), 1), D_PSI_DOT_IDX, reservation)
    )
  ])
)

debug_thread.start()

window.show()
app.exec()
