import os
import shutil
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

class MediaCache:
    def __init__(self, cache_dir: str = None):
        """
        Инициализация кэша медиафайлов
        :param cache_dir: Папка для кэша. По умолчанию %APPDATA%/DMI/cache/media/
        """
        if cache_dir is None:
            appdata = os.getenv('APPDATA')
            cache_dir = os.path.join(appdata, 'DMI', 'cache', 'media')
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # URL для загрузки медиа
        self.media_base_url = "https://raw.githubusercontent.com/DeadlockMods/mods/main/media"
    
    def get_media_path(self, filename: str) -> Optional[str]:
        """
        Получить путь к медиафайлу (скачать если нет в кэше)
        :param filename: Имя файла (например, 'mod_preview.png')
        :return: Путь к локальному файлу или None если ошибка
        """
        cache_path = self.cache_dir / filename
        
        # Если файл есть в кэше и не устарел
        if self._is_cache_valid(cache_path):
            return str(cache_path)
        
        # Скачиваем файл
        try:
            url = f"{self.media_base_url}/{filename}"
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Сохраняем во временный файл
            temp_path = cache_path.with_suffix('.tmp')
            with open(temp_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            
            # Перемещаем в кэш
            temp_path.replace(cache_path)
            return str(cache_path)
            
        except Exception as e:
            print(f"Ошибка при загрузке {filename}: {e}")
            return None
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """
        Проверить актуальность кэша
        :param cache_path: Путь к файлу
        :return: True если кэш актуален
        """
        if not cache_path.exists():
            return False
        
        # Проверяем возраст файла (например, 24 часа)
        max_age = timedelta(hours=24)
        file_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return file_age < max_age
    
    def clear_cache(self):
        """Очистить кэш"""
        shutil.rmtree(self.cache_dir)
        self.cache_dir.mkdir(parents=True)
