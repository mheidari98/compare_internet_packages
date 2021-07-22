import requests
from bs4 import BeautifulSoup

def rightel(allow_limited_packs=False):

    URL = "https://package.rightel.ir/ExtraPackageSales/ProductListToSales/ShowProduct"
    
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all('div',attrs={"class":"col-md-6 col-xl-4 js-product"})

    pack_json = []
    for pack in results:
        temp = {}
        temp['pack-name'] = (pack.h3.text).replace(u'\xa0', u' ').strip().split("\n")[0].strip()
        temp['data-duration'] = (pack.h3.text).replace(u'\xa0', u' ').strip().split("\n")[1].strip()
        temp['time-range'] = pack.find('div', attrs={"class":"package-card__subtitle"}).text
        temp['price'] = pack['data-price']
        temp['volume'] = pack['data-volume']
        pack_json.append(temp)
    if not allow_limited_packs :
        pack_json = list(filter(lambda x : x['time-range'] == "" , pack_json))
    return pack_json