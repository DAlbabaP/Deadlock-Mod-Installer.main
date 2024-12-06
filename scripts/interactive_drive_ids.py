import json
import os
import re

def extract_drive_id(url: str) -> str:
    """Извлекает ID файла из ссылки Google Drive"""
    # Поддерживаем оба формата ссылок
    # https://drive.google.com/file/d/1xyzABC.../view
    # https://drive.google.com/open?id=1xyzABC...
    patterns = [
        r'\/d\/([^\/]+)',  # Формат /d/ID/
        r'id=([^&]+)'      # Формат id=ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ""

def update_mods_json():
    # Загружаем mods.json
    mods_path = os.path.join('data', 'mods.json')
    with open(mods_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Для каждого мода вставьте ссылку на файл с Google Drive")
    print("Просто нажмите Enter чтобы пропустить мод")
    print("Введите 'q' чтобы сохранить и выйти\n")
    
    # Группируем моды по категориям для удобства
    categories = {}
    for mod_id, mod_info in data['mods'].items():
        category = mod_info.get('category', 'other')
        if category not in categories:
            categories[category] = []
        categories[category].append((mod_id, mod_info))
    
    try:
        # Проходим по модам в каждой категории
        for category, mods in categories.items():
            print(f"\n=== {category.upper()} ===")
            for mod_id, mod_info in mods:
                # Пропускаем если уже есть drive_id
                if 'file' in mod_info and 'drive_id' in mod_info['file'] and mod_info['file']['drive_id']:
                    print(f"\nМод уже имеет ID: {mod_id}")
                    continue
                
                print(f"\nМод: {mod_info['title']}")
                print(f"Файл: {mod_info['file']['name']}")
                
                while True:
                    url = input("Вставьте ссылку (Enter для пропуска, 'q' для выхода): ").strip()
                    
                    if not url:  # Пропускаем
                        break
                    if url.lower() == 'q':  # Выходим
                        raise KeyboardInterrupt
                    
                    drive_id = extract_drive_id(url)
                    if drive_id:
                        if 'file' not in mod_info:
                            mod_info['file'] = {}
                        mod_info['file']['drive_id'] = drive_id
                        print(f"ID добавлен: {drive_id}")
                        break
                    else:
                        print("Неверный формат ссылки. Попробуйте снова.")
    
    except KeyboardInterrupt:
        print("\nСохранение изменений...")
    
    # Сохраняем обновленный файл
    with open(mods_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\nФайл mods.json успешно обновлен!")

if __name__ == '__main__':
    update_mods_json()
