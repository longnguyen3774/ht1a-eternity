import requests
from bs4 import BeautifulSoup
import json
import time

def get_instructor_info(username):
    url = f"https://www.coursera.org/instructor/{username}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Name
    ins_name = ""
    h2_tag = soup.find("h2")
    if h2_tag:
        ins_name = h2_tag.get_text(strip=True)

    # Role
    role = ""
    role_tag = None
    if h2_tag:
        role_tag = h2_tag.find_next_sibling("p")
        if role_tag:
            role = role_tag.get_text(strip=True)

    # Organizations
    organizations = []
    if role_tag:
        ul_tag = role_tag.find_next_sibling("ul")
        if ul_tag:
            organizations = [li.get_text(strip=True) for li in ul_tag.find_all("li")]

    # Bio
    bio = ""
    h3_tag = soup.find("h3", string="Bio")
    if h3_tag:
        div_tag = h3_tag.find_next_sibling("div")
        if div_tag:
            bio = div_tag.get_text(strip=True)

    return {
        "ins_name": ins_name,
        "role": role,
        "organizations": organizations,
        "bio": bio
    }

default_info = {
        "ins_name": "",
        "role": "",
        "organizations": "",
        "bio": ""
    }

# Đọc file instructors.json
with open("instructors.json", "r", encoding="utf-8") as f:
    instructors = json.load(f)

# Crawl từng instructor và bổ sung thông tin
for ins in instructors:
    username = ins["username"]
    print(f"Đang xử lý: {username}")
    try:
        info = get_instructor_info(username)
        ins.update(info)
    except Exception as e:
        if "404 Client Error" in str(e):
            print(f"Không tìm thấy {username}, thêm dữ liệu mặc định.")
            ins.update(default_info)
            continue
        else:
            print(f"Lỗi với {username}: {e}")
            break

# Lưu lại instructors.json
with open("instructors_all.json", "w", encoding="utf-8") as f:
    json.dump(instructors, f, ensure_ascii=False, indent=2)

print("✅ Hoàn tất cập nhật instructors.json")
