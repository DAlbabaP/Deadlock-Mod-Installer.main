import os
import requests
from typing import Optional, Tuple

class DriveDownloader:
    def __init__(self):
        """Инициализация загрузчика файлов с Google Drive"""
        self.base_url = "https://drive.google.com/uc?export=download"
    
    def download_file(self, file_id: str, target_path: str, 
                     progress_callback=None) -> Tuple[bool, str]:
        """
        Загрузка файла с Google Drive
        :param file_id: ID файла
        :param target_path: Путь для сохранения
        :param progress_callback: Функция для отображения прогресса
        :return: (успех, сообщение)
        """
        try:
            # Создаем сессию для поддержки больших файлов
            session = requests.Session()
            
            # Получаем параметры для загрузки
            response = session.get(f"{self.base_url}&id={file_id}", 
                                 stream=True)
            response.raise_for_status()
            
            # Проверяем наличие страницы подтверждения для больших файлов
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    response = session.get(f"{self.base_url}&id={file_id}&confirm={value}", 
                                        stream=True)
                    break
            
            # Получаем размер файла
            file_size = int(response.headers.get('content-length', 0))
            
            # Создаем папку если нужно
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Загружаем файл с отображением прогресса
            downloaded = 0
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress = (downloaded / file_size) * 100
                            progress_callback(progress)
            
            return True, "Файл успешно загружен"
            
        except Exception as e:
            return False, f"Ошибка при загрузке: {str(e)}"
