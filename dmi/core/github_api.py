import os
import json
import requests
from typing import Dict, Tuple

class GitHubAPI:
    def __init__(self):
        """Инициализация GitHub API клиента"""
        self.api_url = "https://api.github.com"
        self.raw_url = "https://raw.githubusercontent.com"
        self.repo_owner = "DeadlockMods"  # Владелец репозитория
        self.repo_name = "mods"  # Название репозитория
        self.branch = "main"  # Основная ветка
        
    def check_for_updates(self) -> Tuple[bool, str]:
        """
        Проверка наличия обновлений mods.json
        :return: (есть_обновления, сообщение)
        """
        try:
            # Получаем содержимое удаленного mods.json
            url = f"{self.raw_url}/{self.repo_owner}/{self.repo_name}/{self.branch}/data/mods.json"
            response = requests.get(url)
            response.raise_for_status()
            
            remote_mods = response.json()
            
            # Проверяем локальную версию
            local_path = os.path.join("data", "mods.json")
            if not os.path.exists(local_path):
                return True, "Локальный файл mods.json не найден"
            
            with open(local_path, 'r', encoding='utf-8') as f:
                local_mods = json.load(f)
            
            # Сравниваем версии модов
            has_updates = False
            for mod_id, remote_mod in remote_mods['mods'].items():
                if mod_id not in local_mods['mods']:
                    has_updates = True
                    break
                if remote_mod.get('version') != local_mods['mods'][mod_id].get('version'):
                    has_updates = True
                    break
            
            if has_updates:
                return True, "Доступны обновления модов"
            return False, "Обновления не требуются"
            
        except Exception as e:
            return False, f"Ошибка при проверке обновлений: {str(e)}"
    
    def update_mods_json(self) -> Tuple[bool, str]:
        """
        Загрузка актуальной версии mods.json
        :return: (успех, сообщение)
        """
        try:
            # Скачиваем mods.json
            url = f"{self.raw_url}/{self.repo_owner}/{self.repo_name}/{self.branch}/data/mods.json"
            response = requests.get(url)
            response.raise_for_status()
            
            # Сохраняем файл
            os.makedirs("data", exist_ok=True)
            with open(os.path.join("data", "mods.json"), "w", encoding="utf-8") as f:
                json.dump(response.json(), f, indent=2, ensure_ascii=False)
            
            return True, "Список модов успешно обновлен"
            
        except Exception as e:
            return False, f"Ошибка при обновлении: {str(e)}"
    
    def download_mod(self, mod_path: str, target_path: str) -> Tuple[bool, str]:
        """
        Скачивание файла мода
        :param mod_path: Путь к моду в репозитории
        :param target_path: Путь для сохранения
        :return: (успех, сообщение)
        """
        try:
            # Скачиваем файл мода
            url = f"{self.raw_url}/{self.repo_owner}/{self.repo_name}/{self.branch}/{mod_path}"
            response = requests.get(url)
            response.raise_for_status()
            
            # Создаем папку если нужно
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Сохраняем файл
            with open(target_path, "wb") as f:
                f.write(response.content)
            
            return True, "Мод успешно скачан"
            
        except Exception as e:
            return False, f"Ошибка при скачивании мода: {str(e)}"
