import os
import base64
import json

# Папка с фотографиями
PHOTOS_DIR = "photos"
# Файл для генерации
OUTPUT_FILE = "photos_base64.js"

places_dict = {}

# Проходим по всем файлам в папке photos/
for filename in os.listdir(PHOTOS_DIR):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(PHOTOS_DIR, filename)
        # Конвертируем фото в base64
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        # Создаём data URI
        ext = filename.split('.')[-1].lower()
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        data_uri = f"data:{mime};base64,{encoded}"

        # Разбиваем имя файла по _ для группировки фото в одно место
        # Например: trip_1.jpg и trip_2.jpg → place id = trip
        parts = filename.split('_')
        place_id = parts[0]

        if place_id not in places_dict:
            # Создаём объект места
            places_dict[place_id] = {
                "id": place_id,
                "title": place_id.replace("-", " ").title(),
                "date": "2025-01-01",      # можно менять вручную
                "lat": 59.9386,            # замените на реальные координаты
                "lng": 30.3141,            # замените на реальные координаты
                "text": "",                # можно добавить описание
                "photos": []
            }
        # Добавляем фото в массив
        places_dict[place_id]["photos"].append(data_uri)

# Преобразуем в список
places = list(places_dict.values())

# Генерируем JS-файл
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("const places = ")
    json.dump(places, f, ensure_ascii=False, indent=2)
    f.write(";")

print(f"Генерация {OUTPUT_FILE} завершена. Найдено {len(places)} мест.")
