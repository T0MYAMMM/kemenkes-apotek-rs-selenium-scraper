from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = Options()
#options.add_argument("--headless")

# ------------------- MASUK HALAMAN WEB -------------------#
PATH = "C:\WebDriver\bin\chromedriver.exe"
s = Service(PATH)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(r"C:\Users\Thomas Stefen M\Dropbox\My PC (LAPTOP-VVOKBOQQ)\Documents\All about me\Kalbe Internship\Data\Selenium\extension_5_8_0_0.crx")

#driver = webdriver.Chrome(service=s, options=options, chrome_options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://lewatmana.com/lokasi/fasilitas-kesehatan/rumah-sakit/")

time.sleep(10)

# ------------------- CARI SEARCH PAGE -------------------#
search = driver.find_element(By.XPATH, '//*[@id="poi-search-by-category-query"]')
search.send_keys("")
search.send_keys(Keys.RETURN)


# ------------------- AMBIL ELEMENT SEARCH RESULT -------------------#
hospital_list = []

#page_number = 0

while True:
    wait = WebDriverWait(driver, 10)
    #'/html/body/div[3]/div[1]/div[3]' ini main
    hospitals_left = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.related_poi_left')))
    hospitals_right = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.related_poi_right')))
    hospitals = hospitals_left + hospitals_right

    for hospital in hospitals:
        title_hospital = hospital.find_element(By.TAG_NAME, 'h3')
        title = title_hospital.text
        link = title_hospital.find_element(By.TAG_NAME, 'a').get_attribute('href')
        address = hospital.find_element(By.TAG_NAME, 'p').text.replace('\n', ', ')

        data = {
            'title' : title,
            'link' : link,
            'address' : address
        }

        hospital_list.append(data)

    #print('[' + str(page_number) + ']')    
    print(len(hospital_list))
    

    pagination_items = driver.find_elements(By.CSS_SELECTOR, '#pagination-container ul li')
    item_count = len(pagination_items)

    try:
        next_button_xpath = f'//*[@id="pagination-container"]/ul/li[{item_count}]/a'
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, next_button_xpath))
        )
    except:
        break

    previous_url = driver.current_url
    if next_button.is_enabled() and next_button.is_displayed():
        next_button.click()
        time.sleep(2)  # Tunggu beberapa detik untuk memastikan halaman telah dimuat
        current_url = driver.current_url
        if current_url == previous_url:
            break
    else:
        break

# ------------------- EXPORT CSV -------------------#
with open('data_rumah_sakit_seluruh_indonesia.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # header
    writer.writerow(['title', 'link', 'address'])

    # fill csv
    for data in hospital_list:
        writer.writerow([data['title'], data['link'], data['address']])

#time.sleep(50)
driver.quit()