from PySide6.QtWidgets import QWidget, QHBoxLayout

class PDPannel (QWidget):
  def __init__ (self, p_slider, d_slider):
    super().__init__()
    layout = QHBoxLayout()
    layout.addWidget(p_slider)
    layout.addWidget(d_slider)
    self.setLayout(layout)