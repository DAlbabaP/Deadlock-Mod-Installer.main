import json
import os
from typing import Dict

def get_drive_id(mod_name: str) -> str:
    """
    Здесь вы будете вставлять ID файлов с Google Drive
    Формат: имя_мода: drive_id
    """
    drive_ids = {
        # Пример:
        # "color-blind_friendly": "1xyzABC...",
        # "haze_ball": "1abcXYZ...",
    }
    return drive_ids.get(mod_name, "")

def update_mods_json():
    # Путь к файлу mods.json
    mods_path = os.path.join('data', 'mods.json')
    
    # Загружаем текущий mods.json
    with open(mods_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Обновляем каждый мод-
    for mod_id, mod_info in data['mods'].items():
        # Добавляем drive_id если его нет
        if 'file' in mod_info:
            mod_info['file']['drive_id'] = get_drive_id(mod_id)
            
            # Обновляем путь к файлу (теперь он будет на Google Drive)
            if 'path' in mod_info['file']:
                # Сохраняем оригинальный путь как local_path
                mod_info['file']['local_path'] = mod_info['file']['path']
                # Удаляем старый путь
                del mod_info['file']['path']
    
    # Сохраняем обновленный файл
    with open(mods_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("mods.json успешно обновлен!")
    print("\nТеперь нужно:")
    print("1. Загрузить .vpk файлы на Google Drive")
    print("2. Добавить их ID в словарь drive_ids в этом скрипте")
    print("3. Запустить скрипт снова для обновления mods.json")

if __name__ == '__main__':
    update_mods_json()
