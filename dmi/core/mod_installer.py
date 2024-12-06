import os
import shutil
import re
from .config import Config
from .drive_downloader import DriveDownloader
from typing import Tuple, Dict

class ModInstaller:
    def __init__(self):
        """
        Инициализация установщика модов
        """
        self.config = Config()
        self.drive = DriveDownloader()
        # Путь к папке аддонов будет получен при первом использовании
        self._game_path = None
    
    @property
    def game_path(self) -> str:
        """
        Получение пути к папке аддонов
        Путь запрашивается только при первом обращении
        """
        if self._game_path is None:
            self._game_path = self.config.get_addons_path()
            # Создаем папку если её нет
            if not os.path.exists(self._game_path):
                os.makedirs(self._game_path)
        return self._game_path
    
    def _get_next_pak_number(self) -> str:
        """
        Находит следующий доступный номер для pak файла
        :return: Номер в формате XX (например, '03')
        """
        pattern = re.compile(r'pak(\d+)_dir\.vpk')
        max_number = 0
        
        # Проверяем существование папки
        if not os.path.exists(self.game_path):
            return "01"
        
        # Сканируем существующие pak файлы
        for file in os.listdir(self.game_path):
            match = pattern.match(file)
            if match:
                number = int(match.group(1))
                max_number = max(max_number, number)
        
        # Возвращаем следующий номер в формате XX
        return f"{max_number + 1:02d}"
    
    def install_mod(self, mod_path: str = None, mod_data: Dict[str, str] = None) -> Tuple[bool, str]:
        """
        Установка мода
        :param mod_path: Путь к файлу мода (.vpk)
        :param mod_data: Информация о моде для загрузки с Google Drive
        :return: (успех, сообщение)
        """
        try:
            if mod_path:
                if not os.path.exists(mod_path):
                    return False, "Файл мода не найден"
                
                if not mod_path.endswith('.vpk'):
                    return False, "Файл не является VPK файлом"
                
                # Получаем следующий номер для pak файла
                next_number = self._get_next_pak_number()
                new_filename = f"pak{next_number}_dir.vpk"
                destination = os.path.join(self.game_path, new_filename)
                
                # Создаем папку назначения если её нет
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                
                # Копируем файл с новым именем
                shutil.copy2(mod_path, destination)
                
                return True, f"Мод установлен как {new_filename}"
            elif mod_data:
                # Получаем информацию о файле
                file_info = mod_data['file']
                file_id = file_info['drive_id']
                
                # Путь для сохранения
                target_dir = os.path.join(self.config.game_path, 'game', 'deadlock', 'custom')
                target_path = os.path.join(target_dir, file_info['name'])
                
                # Загружаем файл
                success, message = self.drive.download_file(
                    file_id, 
                    target_path,
                    self.progress_callback
                )
                
                if not success:
                    return False, f"Ошибка загрузки: {message}"
                    
                return True, "Мод успешно установлен"
            else:
                return False, "Не указан путь к моду или информация о моде"
                
        except Exception as e:
            return False, f"Ошибка при установке мода: {str(e)}"
    
    def uninstall_mod(self, pak_filename: str) -> Tuple[bool, str]:
        """
        Удаление мода
        :param pak_filename: Имя pak файла (например, 'pak03_dir.vpk')
        :return: (успех, сообщение)
        """
        try:
            if not pak_filename.startswith('pak') or not pak_filename.endswith('_dir.vpk'):
                return False, "Неверное имя pak файла"
            
            file_path = os.path.join(self.game_path, pak_filename)
            
            if not os.path.exists(file_path):
                return False, "Файл мода не найден"
            
            os.remove(file_path)
            return True, f"Мод {pak_filename} удален"
            
        except Exception as e:
            return False, f"Ошибка при удалении мода: {str(e)}"
    
    def get_installed_mods(self) -> list[str]:
        """
        Получение списка установленных модов
        :return: Список имен установленных pak файлов
        """
        if not os.path.exists(self.game_path):
            return []
            
        pattern = re.compile(r'pak\d+_dir\.vpk')
        return [f for f in os.listdir(self.game_path) if pattern.match(f)]
    
    def is_mod_installed(self, pak_filename: str) -> bool:
        """
        Проверка установлен ли мод
        :param pak_filename: Имя pak файла
        :return: True если мод установлен
        """
        return pak_filename in self.get_installed_mods()
