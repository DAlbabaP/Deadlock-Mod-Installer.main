from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SplashTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Генератор заставки"))
        # TODO: Добавить элементы интерфейса для настройки заставки
