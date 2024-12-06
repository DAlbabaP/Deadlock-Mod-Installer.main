from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog)
from PyQt6.QtCore import Qt
import os

class GamePathDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Путь к игре")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Описание
        description = QLabel(
            "Пожалуйста, укажите путь к папке с игрой Deadlock.\n"
            "Моды будут установлены в папку game/citadel/addons"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Поле для пути
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.browse_btn = QPushButton("Обзор")
        self.browse_btn.clicked.connect(self.browse_path)
        
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Отмена")
        
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Деактивируем OK пока путь не валиден
        self.path_input.textChanged.connect(self.validate_path)
        self.ok_btn.setEnabled(False)
    
    def browse_path(self):
        """Открытие диалога выбора папки"""
        path = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку с игрой Deadlock"
        )
        if path:
            self.path_input.setText(path)
    
    def validate_path(self):
        """Проверка валидности пути"""
        path = self.path_input.text()
        addons_path = os.path.join(path, "game", "citadel", "addons")
        
        # Проверяем существование папки
        is_valid = os.path.exists(path)
        
        # Проверяем что это папка с игрой
        if is_valid:
            is_valid = os.path.exists(os.path.join(path, "game", "citadel"))
        
        # Создаем папку аддонов если её нет
        if is_valid and not os.path.exists(addons_path):
            try:
                os.makedirs(addons_path)
            except:
                is_valid = False
        
        self.ok_btn.setEnabled(is_valid)
    
    def get_path(self) -> str:
        """Получение выбранного пути"""
        return self.path_input.text()
