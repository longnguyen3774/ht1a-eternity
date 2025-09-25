import glob
import json

all_courses = []

# Tìm tất cả file courses_*.json
files = sorted(glob.glob("courses/courses_*.json"))

print(f"📂 Tìm thấy {len(files)} file:", files)

for f in files:
    with open(f, "r", encoding="utf-8") as infile:
        data = json.load(infile)
        all_courses.extend(data)  # nối vào danh sách chung

# Lưu thành file duy nhất
with open("courses_all.json", "w", encoding="utf-8") as outfile:
    json.dump(all_courses, outfile, ensure_ascii=False, indent=2)

print(f"✅ Đã gộp {len(files)} file thành courses_all.json với {len(all_courses)} khóa học")
