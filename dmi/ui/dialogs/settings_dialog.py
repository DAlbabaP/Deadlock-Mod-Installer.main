from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog,
                             QGroupBox, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt
from dmi.core.config import Config
import os

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.config = Config()
        
        layout = QVBoxLayout(self)
        
        # Группа настроек игры
        game_group = QGroupBox("Настройки игры")
        game_layout = QVBoxLayout(game_group)
        
        # Путь к игре
        path_layout = QHBoxLayout()
        path_label = QLabel("Путь к игре:")
        self.path_input = QLineEdit()
        self.path_input.setText(self.config.config["game"]["base_path"])
        self.browse_btn = QPushButton("Обзор")
        self.browse_btn.clicked.connect(self.browse_path)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        game_layout.addLayout(path_layout)
        
        # Статус пути
        self.path_status = QLabel()
        self.path_status.setStyleSheet("color: red;")
        game_layout.addWidget(self.path_status)
        
        layout.addWidget(game_group)
        
        # Группа общих настроек
        general_group = QGroupBox("Общие настройки")
        general_layout = QVBoxLayout(general_group)
        
        # Язык
        language_layout = QHBoxLayout()
        language_label = QLabel("Язык:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "English"])
        self.language_combo.setCurrentText("Русский" if self.config.get_language() == "ru" else "English")
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        general_layout.addLayout(language_layout)
        
        # Проверка обновлений
        self.check_updates = QCheckBox("Проверять обновления при запуске")
        self.check_updates.setChecked(self.config.get_check_updates())
        general_layout.addWidget(self.check_updates)
        
        layout.addWidget(general_group)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Отмена")
        
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
        
        # Валидация при изменении пути
        self.path_input.textChanged.connect(self.validate_path)
        self.validate_path()
    
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
        
        if not path:
            self.path_status.setText("Путь не указан")
            self.ok_btn.setEnabled(False)
            return
        
        if not os.path.exists(path):
            self.path_status.setText("Указанный путь не существует")
            self.ok_btn.setEnabled(False)
            return
        
        if not os.path.exists(os.path.join(path, "game", "citadel")):
            self.path_status.setText("Это не папка с игрой Deadlock")
            self.ok_btn.setEnabled(False)
            return
        
        self.path_status.setText("")
        self.ok_btn.setEnabled(True)
    
    def accept(self):
        """Сохранение настроек"""
        # Сохраняем путь к игре
        self.config.set_game_path(self.path_input.text())
        
        # Сохраняем язык
        self.config.set_language("ru" if self.language_combo.currentText() == "Русский" else "en")
        
        # Сохраняем настройку обновлений
        self.config.set_check_updates(self.check_updates.isChecked())
        
        super().accept()
