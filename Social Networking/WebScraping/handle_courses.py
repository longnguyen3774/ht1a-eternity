import os
import csv
import json

# Thư mục chứa các file CSV
folder_path = 'categories'

# Dictionary kết quả
dict_of_categories = {}

# Duyệt qua tất cả các file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Tạo tên key: loại bỏ "_courses", tách bằng "-", nối bằng " ", viết hoa chữ cái đầu
        base_name = filename.replace('_courses.csv', '')
        key = ' '.join(base_name.split('-')).title()

        # Đọc danh sách URL từ file CSV
        file_path = os.path.join(folder_path, filename)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            urls = [row[0] for row in reader if row]  # Lấy dòng đầu tiên mỗi hàng nếu không rỗng

        # Gán vào dict
        dict_of_categories[key] = urls

# Đọc dữ liệu khóa học
with open('courses_all.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Giả sử dict_of_categories đã có từ bước trước
# Tạo ánh xạ từ URL sang tên danh mục
url_to_category = {}
for category, urls in dict_of_categories.items():
    for url in urls:
        url_to_category[url] = category

# Cập nhật từng khóa học với category ở đúng vị trí
updated_courses = []
for course in courses:
    url = course.get("url")
    name = course.get("name")
    category = url_to_category.get(url)

    # Xử lý skill: loại bỏ "View all skills" nếu có
    skills = course.get("skills").replace(", View all skills", "")
    course["skills"] = skills

    # Tạo dict mới với thứ tự khóa mong muốn
    new_course = {
        "url": url,
        "name": name,
        "category": category
    }

    # Thêm các khóa còn lại
    for key, value in course.items():
        if key not in new_course:
            new_course[key] = value

    if course.get("language") == "English":
        updated_courses.append(new_course)

# Ghi ra file mới
with open('courses_en.json', 'w', encoding='utf-8') as f:
    json.dump(updated_courses, f, ensure_ascii=False, indent=2)

print("Đã cập nhật và lưu file courses_en.json với category ở đúng vị trí.")
