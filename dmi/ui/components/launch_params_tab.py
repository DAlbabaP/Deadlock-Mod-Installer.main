from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class LaunchParamsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Генератор параметров запуска"))
        # TODO: Добавить элементы интерфейса для настройки параметров запуска
