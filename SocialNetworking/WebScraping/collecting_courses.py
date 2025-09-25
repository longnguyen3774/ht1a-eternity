import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import math

# Đọc file CSV chứa danh sách link, không có header
df_links = pd.read_csv("course_links.csv", header=None, names=["url"])

# Chuyển thành list
links = df_links["url"].tolist()

courses = []
chunk_size = 200  # mỗi 200 khóa học thì lưu lại
chunk_index = 24  # đánh số file

for idx, url in enumerate(links[4600:], start=1):
    print(f"[{idx}] Đang xử lý: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Dùng content để tránh lỗi font
        soup = BeautifulSoup(response.content, "html.parser")

        # Tìm instructor links
        instructors = soup.find_all("a", attrs={
            "data-click-key": "unified_description_page.consumer_course_page.click.hero_instructor"
        })
        instructors_list = list({a.get("href", "").replace("/instructor/", "") for a in instructors if a.get("href")})

        # Lấy tên khóa học
        course_name = soup.find("h1")
        course_name = course_name.get_text(strip=True) if course_name else ""

        # Lấy mô tả khóa học
        content_div = soup.find("div", class_="content")
        course_content = content_div.get_text(strip=True) if content_div else ""

        # Lấy "What you'll learn"
        learn_div = soup.find("div", attrs={"data-track-component": "what_you_will_learn_section"})
        if learn_div:
            learn_items = [span.get_text(strip=True) for span in learn_div.find_all("span") if
                           span.get_text(strip=True)]
            what_you_learn = "\n".join(learn_items)
        else:
            what_you_learn = ""

        # Lưu thông tin khóa học
        courses.append({
            "url": url,
            "name": course_name,
            "content": course_content,
            "what_you_learn": what_you_learn,
            "instructors": instructors_list
        })

    except Exception as e:
        print(f"Lỗi khi xử lý {url}: {e}")
        break

    # ======= Checkpoint mỗi 200 khóa học =======
    if idx % chunk_size == 0:
        filename = f"courses_{chunk_index}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(courses, f, ensure_ascii=False, indent=2)
        print(f"💾 Đã lưu {len(courses)} khóa học vào {filename}")
        chunk_index += 1
        courses = []  # reset để lưu tiếp phần sau

# ======= Lưu phần còn lại chưa đủ 200 =======
if courses:
    filename = f"courses_{chunk_index}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu {len(courses)} khóa học vào {filename}")

print("✅ Hoàn tất crawl và lưu dữ liệu")
