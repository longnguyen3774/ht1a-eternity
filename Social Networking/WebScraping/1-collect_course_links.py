import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Các category cần duyệt
categories = [
    'arts-and-humanities',
    'business',
    'computer-science',
    'data-science',
    'health',
    'information-technology',
    'language-learning',
    'math-and-logic',
    'personal-development',
    'physical-science-and-engineering',
    'social-sciences'
]

# Thiết lập Chrome options
options = Options()
options.add_argument("--headless")  # bỏ nếu muốn xem trình duyệt
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_hrefs = set()  # dùng set để loại bỏ trùng lặp ngay từ đầu

try:
    wait = WebDriverWait(driver, 10)

    for category in categories:
        url = f"https://www.coursera.org/browse/{category}"
        print(f"\nĐang xử lý category: {category}")
        driver.get(url)

        while True:
            # --- Chờ phần searchResults ---
            try:
                search_results = wait.until(
                    EC.presence_of_element_located((By.ID, "searchResults"))
                )
            except TimeoutException:
                print("❌ Không tìm thấy searchResults, bỏ qua category này.")
                break

            # Lấy ul và các li
            ul = search_results.find_element(By.TAG_NAME, "ul")
            lis = ul.find_elements(By.TAG_NAME, "li")

            for li in lis:
                try:
                    a_tag = li.find_element(By.TAG_NAME, "a")
                    href = a_tag.get_attribute("href")
                    if href and href.startswith("https://www.coursera.org/learn"):
                        all_hrefs.add(href)
                except NoSuchElementException:
                    pass

            print(f"✅ Category {category} đã thu thập {len(all_hrefs)} link (tạm thời).")

            # --- Tìm và click nút Next ---
            try:
                next_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Go to next page"]'))
                )
                driver.execute_script("arguments[0].click();", next_button)

                # Chờ trang mới load (ul cũ mất đi)
                wait.until(EC.staleness_of(ul))

                time.sleep(2)

                print('Đã qua trang mới!')
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                print(f"⏹ Hết trang trong category {category}.")
                break

        file_name = f"categories/{category}_courses.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for link in sorted(all_hrefs):
                writer.writerow([link])

        print(f"✅ Đã lưu {len(all_hrefs)} link khóa học vào {file_name}")

        all_hrefs = set()

finally:
    driver.quit()
