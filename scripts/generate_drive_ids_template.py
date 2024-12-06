import json
import os
from typing import Dict

def generate_template():
    # Загружаем mods.json
    mods_path = os.path.join('data', 'mods.json')
    with open(mods_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Создаем словарь для drive_ids
    drive_ids = {}
    
    # Группируем моды по категориям
    categories: Dict[str, list] = {}
    
    for mod_id, mod_info in data['mods'].items():
        category = mod_info.get('category', 'other')
        if category not in categories:
            categories[category] = []
        
        # Добавляем информацию о моде
        categories[category].append({
            'id': mod_id,
            'title': mod_info['title'],
            'file_name': mod_info['file']['name'],
            'drive_id': ''  # Здесь будет ID
        })
    
    # Создаем файл с шаблоном
    template_path = 'scripts/drive_ids_template.py'
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write('"""\nШаблон для ID файлов с Google Drive.\n')
        f.write('Для каждого мода вставьте ID из ссылки на файл.\n')
        f.write('Пример ссылки: https://drive.google.com/file/d/1xyzABC.../view\n')
        f.write('ID это часть между /d/ и /view\n"""\n\n')
        
        f.write('drive_ids = {\n')
        
        # Записываем моды по категориям
        for category, mods in categories.items():
            f.write(f'    # {category.upper()}\n')
            for mod in mods:
                f.write(f'    "{mod["id"]}": "",  # {mod["title"]} ({mod["file_name"]})\n')
            f.write('\n')
        
        f.write('}\n')
    
    print(f"Шаблон создан в {template_path}")
    print("Заполните drive_ids['mod_id'] = 'ID' для каждого мода")
    print("После этого можно запустить update_mods_json.py")

if __name__ == '__main__':
    generate_template()
