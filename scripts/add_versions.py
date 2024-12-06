import json
import os

# Загружаем mods.json
with open(os.path.join('data', 'mods.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

# Добавляем версию для каждого мода
for mod_id in data['mods']:
    if 'version' not in data['mods'][mod_id]:
        data['mods'][mod_id]['version'] = '1.0'

# Сохраняем обновленный файл
with open(os.path.join('data', 'mods.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Версии успешно добавлены!")
