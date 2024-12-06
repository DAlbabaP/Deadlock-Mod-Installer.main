from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QScrollArea, QLabel, QPushButton, QGridLayout,
                             QFrame, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage
from dmi.core.mod_installer import ModInstaller
from dmi.core.media_cache import MediaCache
import os

class ModCard(QFrame):
    def __init__(self, mod_data, parent=None):
        super().__init__(parent)
        self.mod_data = mod_data
        self.mod_installer = ModInstaller()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedSize(300, 400)
        
        layout = QVBoxLayout(self)
        
        # Превью мода
        preview = QLabel()
        preview.setFixedSize(280, 200)
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if mod_data.get('media', {}).get('preview'):
            preview_path = os.path.join('media', mod_data['media']['preview'])
            if os.path.exists(preview_path):
                pixmap = QPixmap(preview_path)
                preview.setPixmap(pixmap.scaled(280, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            preview.setText("Нет превью")
        
        layout.addWidget(preview)
        
        # Информация о моде
        info_layout = QVBoxLayout()
        
        title = QLabel(mod_data.get('title', 'Без названия'))
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(title)
        
        author = QLabel(f"Автор: {mod_data.get('author', 'Неизвестен')}")
        info_layout.addWidget(author)
        
        category = QLabel(f"Категория: {mod_data.get('category', '')}")
        if mod_data.get('hero'):
            category.setText(f"{category.text()} - {mod_data['hero']}")
        info_layout.addWidget(category)
        
        description = QLabel(mod_data.get('descriptions', {}).get('ru', ''))
        description.setWordWrap(True)
        description.setFixedHeight(80)
        info_layout.addWidget(description)
        
        layout.addLayout(info_layout)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        # Кнопка установки/удаления
        self.install_btn = QPushButton()
        self.install_btn.clicked.connect(self.toggle_mod)
        buttons_layout.addWidget(self.install_btn)
        
        if mod_data.get('media', {}).get('video'):
            preview_btn = QPushButton("Превью")
            preview_btn.clicked.connect(self.show_preview)
            buttons_layout.addWidget(preview_btn)
        
        layout.addLayout(buttons_layout)
        
        # Обновляем состояние кнопки
        self.update_button_state()
    
    def update_button_state(self):
        """Обновление состояния кнопки установки"""
        mod_filename = self.mod_data['file']['name']
        if self.mod_installer.is_mod_installed(mod_filename):
            self.install_btn.setText("Удалить")
            self.install_btn.setStyleSheet("background-color: #ff4444;")
        else:
            self.install_btn.setText("Установить")
            self.install_btn.setStyleSheet("background-color: #44ff44;")
    
    def toggle_mod(self):
        """Установка или удаление мода"""
        try:
            mod_filename = self.mod_data['file']['name']
            
            if self.mod_installer.is_mod_installed(mod_filename):
                # Удаляем мод
                success, message = self.mod_installer.uninstall_mod(mod_filename)
                if success:
                    QMessageBox.information(self, "Успех", f"Мод успешно удален")
                else:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении мода: {message}")
            else:
                # Устанавливаем мод
                mod_path = os.path.join('mods', self.mod_data['file']['path'])
                success, message = self.mod_installer.install_mod(mod_path)
                if success:
                    QMessageBox.information(self, "Успех", f"Мод успешно установлен")
                else:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка при установке мода: {message}")
            
            # Обновляем состояние кнопки
            self.update_button_state()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Непредвиденная ошибка: {str(e)}")
    
    def show_preview(self):
        """Показ превью/видео мода"""
        video_url = self.mod_data.get('media', {}).get('video')
        if video_url:
            # TODO: Реализовать показ превью/видео
            QMessageBox.information(self, "Превью", f"Видео доступно по ссылке: {video_url}")


class ModsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.mods_data = []
        self.media_cache = MediaCache()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Создаем область прокрутки
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Контейнер для карточек модов
        self.mods_container = QWidget()
        self.grid_layout = QGridLayout(self.mods_container)
        self.grid_layout.setSpacing(20)
        
        scroll.setWidget(self.mods_container)
        layout.addWidget(scroll)
    
    def update_mods(self, mods_data):
        """Обновление списка модов"""
        self.mods_data = mods_data
        self.refresh_view()
    
    def filter_mods(self, search_text, category):
        """Фильтрация модов по поиску и категории"""
        filtered_mods = []
        
        for mod_data in self.mods_data:
            # Фильтр по категории
            if category != "Все категории" and mod_data['category'].lower() != category.lower():
                continue
            
            # Фильтр по поиску
            search_in = [
                mod_data.get('title', ''),
                mod_data.get('author', ''),
                mod_data.get('descriptions', {}).get('ru', ''),
                mod_data.get('descriptions', {}).get('en', '')
            ]
            
            if not any(search_text in text.lower() for text in search_in):
                continue
            
            filtered_mods.append(mod_data)
        
        self.refresh_view(filtered_mods)
    
    def refresh_view(self, mods_data=None):
        """Обновление отображения модов"""
        # Очищаем текущее отображение
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Если не переданы моды для отображения, используем все
        if mods_data is None:
            mods_data = self.mods_data
        
        # Добавляем карточки модов
        row = 0
        col = 0
        max_cols = 3
        
        for mod_data in mods_data:  
            card = ModCard(mod_data)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def resizeEvent(self, event):
        """Обработка изменения размера окна"""
        super().resizeEvent(event)
        self.refresh_view()
