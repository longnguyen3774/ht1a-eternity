import json

# ====== B1: Đọc dữ liệu courses_all.json ======
with open("courses_all.json", "r", encoding="utf-8") as f:
    courses = json.load(f)

# ====== B2: Tổng hợp instructors và gán ID ======
all_instructors = sorted({inst for c in courses for inst in c["instructors"]})
instructor2id = {username: idx for idx, username in enumerate(all_instructors)}

# Lưu instructors.json
instructors_data = [{"id": idx, "username": username} for username, idx in instructor2id.items()]
with open("instructors.json", "w", encoding="utf-8") as f:
    json.dump(instructors_data, f, ensure_ascii=False, indent=2)
