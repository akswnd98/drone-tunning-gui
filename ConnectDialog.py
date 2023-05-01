from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
  QPushButton, QWidget, QVBoxLayout, 
  QHBoxLayout, QLineEdit, QLabel, QDialog
)

class ConnectDialog (QDialog):
  def __init__ (self, reservation):
    super().__init__ ()
    self.setWindowTitle('connect')
    self.setFixedSize(QSize(300, 100))
    v_layout = QVBoxLayout()
    h_layout = QHBoxLayout()
    self.setLayout(v_layout)
    upper_pannel = QWidget()
    upper_pannel.setLayout(h_layout)
    self.push_button = QPushButton('connect')
    v_layout.addWidget(upper_pannel)
    v_layout.addWidget(self.push_button)
    port_label = QLabel('port: ')
    self.port_edit = QLineEdit()
    baudrate_label = QLabel('baudrate: ')
    self.baudrate_edit = QLineEdit()
    h_layout.addWidget(port_label)
    h_layout.addWidget(self.port_edit)
    h_layout.addWidget(baudrate_label)
    h_layout.addWidget(self.baudrate_edit)
    
    self.reservation = reservation

    self.push_button.clicked.connect(self.handle_push_button_click)
  
  def handle_push_button_click (self):
    self.reservation.connect(self.port_edit.text(), int(self.baudrate_edit.text()))
    self.close()