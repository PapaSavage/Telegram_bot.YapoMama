import requests
import os
from bs4 import BeautifulSoup as BS


def pars(url, url1='https://yaponomaniya.com'):
    r = requests.get(url)
    html = BS(r.content, 'html.parser')

    # example url - https://yaponomaniya.com/assorty check_up kind of type_food

    b = []
    for el in html.select(".product-items > .set"):
        t = el.select(".price.new.h3")
        b.append(t[0].text)

    p = [i.replace('\n', '') for i in b]
    p = [i.replace('\xa0', '') for i in b]

    w = []
    for el in html.select(".product-items > .set"):
        t = el.select(".product-title")
        w.append(t[0].text)

    d = [i.replace('"', '') for i in [i.replace('\n', '') for i in w]]

    q = []
    for el in html.select(".product-items > .set"):
        t = el.select(".product-desc")
        q.append(t[0].text)

    z = [i.strip() for i in [i.replace('\n', '') for i in q]]

    list = []
    listurl = []
    # основная ссылка

    URL_TEMPLATE = url
    r = requests.get(URL_TEMPLATE)
    html = BS(r.text, "html.parser")
    t = html.find_all('div', class_='text')

    i = 0
    quotes = html.find_all('img', class_='product-img')
    for quote in quotes:
        url = url1 + (quote.get('src'))
        listurl.append(f"photo/{(d[i].strip())}.jpg")
        img_data = requests.get(url).content
        k = os.path.join(f"photo/{(d[i].strip())}.jpg")
        with open(k, 'wb') as handler:
            handler.write(img_data)
        i += 1

    a = []
    for i in range(len(w)):
        a.insert(i, [d[i], p[i], z[i], listurl[i]])
    return a
# print(len(pars("https://yaponomaniya.com/assorty")))
