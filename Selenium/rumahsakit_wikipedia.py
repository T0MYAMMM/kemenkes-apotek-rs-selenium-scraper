from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv

options = Options()

# ------------------- MASUK HALAMAN WEB -------------------#
PATH = "C:\WebDriver\bin\chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(r"C:\Users\Thomas Stefen M\Dropbox\My PC (LAPTOP-VVOKBOQQ)\Documents\All about me\Kalbe Internship\Data\Selenium\extension_5_8_0_0.crx")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://id.wikipedia.org/wiki/Daftar_rumah_sakit_di_Indonesia")

# wait for extension installation 
time.sleep(10)

# ------------------- Find Table -------------------#
tables = driver.find_elements(By.TAG_NAME, "table")
#table = driver.find_element(By.CLASS_NAME, 'wikitable')

hospital_list = []
for table in tables:
    rows = table.find_elements(By.TAG_NAME, 'tr')
    header = [th.text for th in rows[0].find_elements(By.TAG_NAME, 'th')]
    data = []
    for row in rows[1:]:
        row_data = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
        if len(row_data) == len(header):
            data.append(row_data)
    
    df = pd.DataFrame(data, columns=header)
    
    print(df)
    print('\n')
    hospital_list.append(df)


list_table_name = ['Berdasarkan Penyelenggara', 'Berdasarkan Jenis Pelayanan', 'Aceh', 'Bali', 'Banten', 'Bengkulu', 'Daerah Istimewa Yogyakarta', 'Daerah Khusus Ibu kota Jakarta', 'Jakarta Barat', 'Jakarta Pusat', 'Jakarta Selatan', 'Jakarta Timur', 'Jakarta Utara', 'Kepulauan Seribu', 'Gorontalo', 'Jambi', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'additional jatim', 'Kalimantan Barat', 'Kalimantan Selatan', 'Kalimantan Tengah', 'Kalimantan Timur', 'Kalimantan Utara', 'Kepulauan Bangka Belitung', 'Kepulauan Riau', 'Lampung', 'Maluku', 'Maluku Utara', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'nyampah', 'Papua', 'Papua Barat', 'Riau', 'Sulawesi Barat', 'Sulawesi Selatan', 'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Utara', 'Sumatera Barat', 'Sumatera Selatan', 'Sumatera Utara', 'menurut provinsi', 'di asia']

print('check')
print(len(hospital_list))
print(len(list_table_name))


for index, df in enumerate(hospital_list):
    file_name = f"tabel_{list_table_name[index]}.csv"
    df.to_csv(file_name, index=False)



driver.quit()