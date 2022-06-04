import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

#connect mongodb
client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client["FilmArsivSistemi"] # db adı
filmTable = db["new_film_data"] # FilmArsivsistemi db'sinde bulunan new_film_data collection'ı çağırılır

# 30 sayfadan oluşan en iyi filmler listesini parse etmek için for döngüsü kullanılır
for i in range (1,31):
    if i==1:
        URL = "https://www.beyazperde.com/filmler/en-iyi-filmler/" # en iyi filmler sayfası için ilk sayfa url'i
    else:
        URL = f"https://www.beyazperde.com/filmler/en-iyi-filmler/?page={i}" # en iyi filmlerin gösterildiği diğer sayfaların url'i

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser") # parse yapmak için BeautifulSoup çağırılır
    results = soup.find_all("a", class_="meta-title-link") # url sayfasındaki sınıfı meta-title-link olan tüm a tag'i değerleri
    for res in results:
        film_url = res["href"] # a tag'ininde bulunan href değeri alınır. Bu href içerisinde filmin özetine ukaşacağımız link bulunur
        film_name = res.text.strip() # a tag'inden filmin adı alınır

        url_for_summary = "https://www.beyazperde.com"+film_url # özete ulaşmak için gidilecek link
        page_for_summary = requests.get(url_for_summary)
        soup_for_summary = BeautifulSoup(page_for_summary.content, "html.parser")
        res_for_summary = soup_for_summary.find("div", class_="content-txt") # sınıfı content-txt olan div tag'i alınır
        summary_results = res_for_summary.text.strip() # div tag'inden özet yazısı çekilir

        filmTable.insert_one({"Film Adı": film_name, "Özet": summary_results}) # film adı ve özetleri mongodb'deki new_film_data collection'ına eklenir

        print(f"film adı = {film_name}  özet = {summary_results}") # film adı ve özet ekrana yazdırılır
