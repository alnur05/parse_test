import requests
from bs4 import BeautifulSoup

def get_html(url):
    result = requests.get(url)
    return result.text


def get_date(html):
    soup = BeautifulSoup(html, 'lxml')
    # div = soup.find('div').get('id')
    # h2 = soup.findAll('div').get('screenshots')
    # for h in h2:
    #     print(h)
    section = soup.findAll('section', {'class': 'plugin-section'})[1]
    plugins = section.findAll('article')

    for plagin in plugins:
        h3 = plagin.find('h3')
        rating = plagin.find('span', {'class' : 'rating-count'})
        print(h3.text, rating.text)


def main():
    html = get_html("https://ru.wordpress.org/plugins/")
    data = get_date(html)


if __name__ == '__main__':
    main()