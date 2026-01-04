import os
import base64

# Папка с фотографиями
photos_folder = "photos"
# JS-файл с массивом places
output_js = "photos_base64.js"

places_array = []

for filename in os.listdir(photos_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(photos_folder, filename)
        with open(path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
            ext = filename.split('.')[-1].lower()
            place = f"""{{
    id: "{filename}",
    title: "{filename.split('.')[0]}",
    date: "2025-02-04",
    lat: 59.9386,
    lng: 30.3141,
    text: "Описание для {filename}",
    photo: "data:image/{ext};base64,{img_b64}"
}}"""
            places_array.append(place)

with open(output_js, "w", encoding="utf-8") as f:
    f.write("const places = [\n")
    f.write(",\n".join(places_array))
    f.write("\n];\n")

print(f"{output_js} успешно создан! Всего мест: {len(places_array)}")
