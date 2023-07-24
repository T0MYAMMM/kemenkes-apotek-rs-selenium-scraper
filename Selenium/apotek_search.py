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
driver.get("https://lewatmana.com/lokasi/fasilitas-kesehatan/apotek/")

time.sleep(10)

# ------------------- CARI SEARCH PAGE -------------------#
search = driver.find_element(By.XPATH, '//*[@id="poi-search-by-category-query"]')
search.send_keys("")
search.send_keys(Keys.RETURN)


# ------------------- AMBIL ELEMENT SEARCH RESULT -------------------#
apotek_list = []

#page_number = 0

while True:
    wait = WebDriverWait(driver, 10)
    #'/html/body/div[3]/div[1]/div[3]' ini main
    apoteks_left = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.related_poi_left')))
    apoteks_right = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.related_poi_right')))
    apoteks = apoteks_left + apoteks_right

    for apotek in apoteks:
        title_apotek = apotek.find_element(By.TAG_NAME, 'h3')
        title = title_apotek.text
        link = title_apotek.find_element(By.TAG_NAME, 'a').get_attribute('href')
        address = apotek.find_element(By.TAG_NAME, 'p').text.replace('\n', ', ')

        data = {
            'title' : title,
            'link' : link,
            'address' : address
        }

        apotek_list.append(data)

    #print('[' + str(page_number) + ']')    
    print(len(apotek_list))
    #//*[@id="pagination-container"]/ul/li[9]/a
    # halaman 7 : //*[@id="pagination-container"]/ul/li[15]/a
    # halaman 8 : //*[@id="pagination-container"]/ul/li[16]/a
    # halaman 9 : //*[@id="pagination-container"]/ul/li[16]/a
    # halaman 10 : //*[@id="pagination-container"]/ul/li[15]/a
    # halaman 11 : //*[@id="pagination-container"]/ul/li[16]/a
    # halaman 12 : //*[@id="pagination-container"]/ul/li[16]/a

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
with open('output_all.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # header
    writer.writerow(['title', 'link', 'address'])

    # fill csv
    for data in apotek_list:
        writer.writerow([data['title'], data['link'], data['address']])

#time.sleep(50)
driver.quit()