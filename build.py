import os
import base64
import json

PHOTOS_DIR = "photos"
OUTPUT_FILE = "photos_base64.js"

# Загружаем существующий файл, если есть, чтобы сохранить ручные изменения
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        if content.strip().startswith("const places"):
            # извлекаем JSON после "const places ="
            existing_places = json.loads(content[content.find("["):content.rfind("]")+1])
        else:
            existing_places = []
else:
    existing_places = []

# Создаём словарь по id для быстрого поиска
places_dict = {p['id']: p for p in existing_places}

# Проходим по файлам в папке photos/
for filename in os.listdir(PHOTOS_DIR):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(PHOTOS_DIR, filename)
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        ext = filename.split('.')[-1].lower()
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        data_uri = f"data:{mime};base64,{encoded}"

        # id = имя до первого _
        place_id = filename.split('_')[0]

        if place_id in places_dict:
            # Если место уже есть, просто добавляем фото в массив
            if 'photos' not in places_dict[place_id]:
                places_dict[place_id]['photos'] = []
            if data_uri not in places_dict[place_id]['photos']:
                places_dict[place_id]['photos'].append(data_uri)
        else:
            # Новое место — создаём объект с дефолтными данными
            places_dict[place_id] = {
                "id": place_id,
                "title": place_id.replace("-", " ").title(),
                "date": "2025-01-01",  # можно редактировать вручную позже
                "lat": 59.9386,        # координаты можно поменять вручную
                "lng": 30.3141,
                "text": "",
                "photos": [data_uri]
            }

# Сохраняем обратно в JS-файл
places = list(places_dict.values())
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("const places = ")
    json.dump(places, f, ensure_ascii=False, indent=2)
    f.write(";")

print(f"Генерация {OUTPUT_FILE} завершена. Всего мест: {len(places)}")
