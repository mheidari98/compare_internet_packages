import requests
from bs4 import BeautifulSoup

def irancell(allow_limited_packs=False):

    URL = "https://irancell.ir/o/1001/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86%D8%B3%D9%84-%D8%A8%D8%B3%D8%AA%D9%87-%D9%87%D8%A7%DB%8C-%D8%A7%DB%8C%D9%86%D8%AA%D8%B1%D9%86%D8%AA-%D9%87%D9%85%D8%B1%D8%A7%D9%87"
        
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