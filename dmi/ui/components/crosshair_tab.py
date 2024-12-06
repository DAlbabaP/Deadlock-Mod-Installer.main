from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CrosshairTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Генератор прицела"))
        # TODO: Добавить элементы интерфейса для настройки прицела
