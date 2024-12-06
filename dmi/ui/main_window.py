from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox,
                             QStatusBar, QMessageBox, QTabWidget, QHBoxLayout,
                             QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .components.mods_tab import ModsTab
from .components.launch_params_tab import LaunchParamsTab
from .components.maps_tab import MapsTab
from .components.crosshair_tab import CrosshairTab
from .components.splash_tab import SplashTab
from .dialogs.settings_dialog import SettingsDialog
from .dialogs.game_path_dialog import GamePathDialog
from ..core.config import Config
from ..core.mod_scanner import ModScanner
from ..core.github_api import GitHubAPI
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.config = Config()
        self.github = GitHubAPI()
        
        # Проверяем путь к игре при запуске
        if not self.check_game_path():
            # Если путь не указан или неверный, показываем диалог
            if not self.request_game_path():
                # Если пользователь отменил выбор пути, закрываем программу
                self.close()
                return
        
        self.init_ui()
        
        # Обновляем список модов
        self.refresh_mods()
        
        # Проверяем обновления при запуске
        self.check_updates()
    
    def init_ui(self):
        # Основные настройки окна
        self.setWindowTitle("Deadlock Mod Installer 2.0")
        self.setMinimumSize(1024, 768)
        
        # Инициализация сканера модов
        self.mod_scanner = ModScanner('b:/Projects/DMI 2.0')
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем главный layout
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем верхнюю панель с кнопками
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Кнопка настроек
        self.settings_btn = QPushButton("Настройки")
        self.settings_btn.clicked.connect(self.open_settings)
        toolbar_layout.addWidget(self.settings_btn)
        
        # Кнопка обновления
        self.update_btn = QPushButton("Проверить обновления")
        self.update_btn.clicked.connect(self.check_updates)
        toolbar_layout.addWidget(self.update_btn)
        
        # Растягивающийся разделитель
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar_layout.addItem(spacer)
        
        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск модов...")
        self.search_input.textChanged.connect(self.filter_mods)
        toolbar_layout.addWidget(self.search_input)
        
        # Выпадающий список категорий
        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        self.category_combo.addItem("Heroes")
        self.category_combo.addItem("Interface")
        self.category_combo.addItem("Sounds")
        self.category_combo.addItem("Game")
        self.category_combo.addItem("Post-processing")
        self.category_combo.currentTextChanged.connect(self.filter_mods)
        toolbar_layout.addWidget(self.category_combo)
        
        main_layout.addWidget(toolbar)
        
        # Добавляем вкладку с модами
        self.tabs = QTabWidget()
        self.mods_tab = ModsTab()
        self.tabs.addTab(self.mods_tab, "Моды")
        self.tabs.addTab(LaunchParamsTab(), "Параметры запуска")
        self.tabs.addTab(MapsTab(), "Карты")
        self.tabs.addTab(CrosshairTab(), "Прицел")
        self.tabs.addTab(SplashTab(), "Заставка")
        main_layout.addWidget(self.tabs)
        
        # Создаем статус бар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
    
    def check_game_path(self) -> bool:
        """
        Проверка и запрос пути к игре если нужно
        :return: True если путь установлен
        """
        try:
            self.config.get_addons_path()
            return True
        except ValueError:
            # Путь не установлен, показываем диалог
            dialog = GamePathDialog(self)
            if dialog.exec():
                # Путь выбран
                self.config.set_game_path(dialog.get_path())
                return True
            else:
                # Диалог отменен
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Путь к игре не указан. Программа будет закрыта."
                )
                return False
    
    def request_game_path(self) -> bool:
        """
        Запрос пути к игре у пользователя
        :return: True если путь выбран
        """
        dialog = GamePathDialog(self)
        if dialog.exec():
            # Путь выбран
            self.config.set_game_path(dialog.get_path())
            return True
        else:
            # Диалог отменен
            return False
    
    def refresh_mods(self):
        """Обновление списка модов"""
        self.statusBar.showMessage("Обновление списка модов...")
        mods_data = self.mod_scanner.scan_mods()
        self.mods_tab.update_mods(mods_data["mods"])  # Передаем список модов
        self.statusBar.showMessage("Список модов обновлен", 3000)
    
    def filter_mods(self):
        """Фильтрация модов по поиску и категории"""
        search_text = self.search_input.text().lower()
        category = self.category_combo.currentText()
        self.mods_tab.filter_mods(search_text, category)
    
    def check_updates(self):
        """Проверка обновлений модов"""
        self.statusBar.showMessage("Проверка обновлений...")
        has_updates, message = self.github.check_for_updates()
        
        if has_updates:
            reply = QMessageBox.question(
                self,
                "Доступно обновление",
                f"{message}\nХотите обновить список модов?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success, update_msg = self.github.update_mods_json()
                if success:
                    self.refresh_mods()
                    QMessageBox.information(self, "Успех", update_msg)
                else:
                    QMessageBox.warning(self, "Ошибка", update_msg)
        else:
            self.statusBar.showMessage(message, 3000)
    
    def open_settings(self):
        """Открытие окна настроек"""
        from .dialogs.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        if dialog.exec():
            # Настройки сохранены, обновляем моды
            self.refresh_mods()
