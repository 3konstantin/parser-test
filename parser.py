import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST1 = 'https://www.toy.ru'
HOST = 'https://www.toy.ru/?utm_source=admitad&utm_medium=cpa&admitad_uid=a76a1a184f8ea6e8a4d7752908293c22' \
       '&utm_campaign=442763&utm_content=a76a1a184f8ea6e8a4d7752908293c22 '
URL = 'https://www.toy.ru/catalog/boy_lego/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.69 Safari/537.36 '
}


# функция которая забирает со страницы по указанаом url(адресу) и params(параметрам) html
def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# функция получения контента
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col-12 col-sm-6 col-md-6 col-lg-4 col-xl-4 my-2')
    cards = []

    # Проверочная
    # print(items)
    # логика для отдельного складывания каждой позиции
    # цикл разбивает по отедльному items в словарь cards
    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='col-12').find('a').find('img').get('title'),
                'link_product': HOST1 + item.find('div', class_='col-12').find('a').get('href'),
                'brand': item.find('div', class_='col-12').find('a').get('gtm-brand'),
                'card_img': HOST1 + item.find('img', class_='img-fluid d-none d-sm-inline').get('data-original'),
                'text': item.find('a', class_='d-block p-1 product-name gtm-click').get_text(strip=True)
            }
        )
    return cards


# проверочная
# html = get_html(URL)
# print(get_content(html.text))

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['название продукта', 'сылка на продукт', 'бренд', 'сылка на картинку', 'техт для проверки'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['brand'], item['card_img'], item['text']])


# функция обработка кода и последовательного выполнения
def parser():
    PAGENATION = input('Укажите колво страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Пропарсил страницу {page} ')
            html = get_html(URL, params={'PAGEN_8': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        print('Я СДЕЛАЛ НАЧАЛЬНИКА')

        pass
    else:
        print('error')


parser()
