import os
import json
from typing import Dict, List

class ModScanner:
    def __init__(self, base_path: str):
        """
        Инициализация сканера модов
        :param base_path: Базовый путь к папке с программой
        """
        self.base_path = base_path
        self.mods_json_path = os.path.join(base_path, 'data', 'mods.json')
        self.mods_data = {}
        self.categories = set()
        self.heroes = set()
    
    def scan_mods(self) -> Dict:
        """
        Загрузка информации о модах из mods.json
        :return: Словарь с информацией о модах
        """
        try:
            with open(self.mods_json_path, 'r', encoding='utf-8') as f:
                self.mods_data = json.load(f)
            
            # Преобразуем словарь модов в список для удобства
            mods_list = []
            for mod_id, mod_info in self.mods_data.get("mods", {}).items():
                # Добавляем id в информацию о моде
                mod_info["id"] = mod_id
                mods_list.append(mod_info)
                
                # Собираем категории и героев
                if "category" in mod_info:
                    self.categories.add(mod_info["category"])
                if "hero" in mod_info:
                    self.heroes.add(mod_info["hero"])
            
            # Заменяем словарь модов на список
            self.mods_data["mods"] = mods_list
            
        except Exception as e:
            print(f"Ошибка при загрузке модов: {str(e)}")
            self.mods_data = {"mods": []}
        
        return self.mods_data
    
    def get_categories(self) -> List[str]:
        """
        Получение списка категорий
        :return: Список категорий
        """
        return sorted(list(self.categories))
    
    def get_heroes(self) -> List[str]:
        """
        Получение списка героев
        :return: Список героев
        """
        return sorted(list(self.heroes))
    
    def filter_mods(self, query: str = "", category: str = "") -> List[Dict]:
        """
        Фильтрация модов по запросу и категории
        :param query: Поисковый запрос
        :param category: Категория для фильтрации
        :return: Отфильтрованный список модов
        """
        filtered_mods = []
        query = query.lower()
        
        for mod in self.mods_data.get('mods', []):
            # Фильтр по категории
            if category and category != "Все":
                if mod.get('category') != category:
                    continue
            
            # Фильтр по поиску
            if query:
                title = mod.get('title', '').lower()
                desc = mod.get('descriptions', {}).get('ru', '').lower()
                author = mod.get('author', '').lower()
                hero = mod.get('hero', '').lower()
                
                if not (query in title or query in desc or 
                       query in author or query in hero):
                    continue
            
            filtered_mods.append(mod)
        
        return filtered_mods

if __name__ == '__main__':
    # Пример использования
    scanner = ModScanner('b:/Projects/DMI 2.0')
    scanner.scan_mods()
