import os
import json
from typing import Any, Dict

class Config:
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Если путь не указан, используем путь по умолчанию
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_path = os.path.join(base_dir, 'data', 'config.json')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Если файл не найден, создаем конфигурацию по умолчанию
            default_config = {
                "game_path": "",
                "settings": {
                    "language": "ru",
                    "check_updates": True
                }
            }
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Dict[str, Any] = None) -> None:
        """Сохранение конфигурации в файл"""
        if config is None:
            config = self.config
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_addons_path(self) -> str:
        """
        Получение пути к папке аддонов
        :return: Полный путь к папке аддонов
        :raises ValueError: Если путь к игре не настроен
        """
        game_path = self.get_game_path()
        if not game_path:
            raise ValueError("Game path is not set")
        return os.path.join(game_path, "game", "citadel", "addons")

    def get_game_path(self) -> str:
        """
        Получение пути к папке игры
        :return: Путь к папке игры или пустая строка если не настроен
        """
        return self.config.get("game_path", "")

    def set_game_path(self, path: str):
        """
        Установка пути к папке игры
        :param path: Путь к папке игры
        """
        # Убираем второй Deadlock из пути если он есть
        if path.lower().endswith('\\deadlock\\deadlock'):
            path = path[:-9]
        
        self.config["game_path"] = path
        self._save_config()
    
    def get_language(self) -> str:
        """Получение текущего языка"""
        return self.config["settings"]["language"]
    
    def set_language(self, language: str) -> None:
        """Установка языка"""
        self.config["settings"]["language"] = language
        self._save_config()
    
    def get_check_updates(self) -> bool:
        """Получение настройки проверки обновлений"""
        return self.config["settings"]["check_updates"]
    
    def set_check_updates(self, check: bool) -> None:
        """Установка настройки проверки обновлений"""
        self.config["settings"]["check_updates"] = check
        self._save_config()
