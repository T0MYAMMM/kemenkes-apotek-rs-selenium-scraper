from bs4 import BeautifulSoup
import requests

'''
with open("index.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")

tags = doc.find_all("p")[0]

print(tags.find_all("b"))'''

url = "https://lewatmana.com/lokasi/fasilitas-kesehatan/apotek/"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

apotek = doc.find_all(te='p')
print(apotek)

