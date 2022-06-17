import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd


def repetitive(links, urls):
    for link in links:
        if link.a['href'] in urls:
            return True
    return False


def scrap_year(year):
    print(year)
    page = 50
    scraped_data = []
    url_list = []

    while True:
        page += 1
        main_page_url = f'https://www.irna.ir/page/archive.xhtml?mn=3&wide=0&dy=25&ms=0&pi={page}&yr={year}'
        html = requests.get(main_page_url).content
        soup = BeautifulSoup(html, features='html.parser')
        links = soup.find_all('h3')
        linkNumbers = len(links) - 41

        if repetitive(links, url_list):
            break

        for link in tqdm(links):
            page_url = 'https://www.irna.ir/' + link.a['href']
            url_list.append(link.a['href'])
            linkNumbers -= 1

            try:
                article = Article(page_url)
                article.download()
                article.parse()
                scraped_data.append({'text': article.text})
            except:
                print(f'Failed to process page: {page_url}')
            if linkNumbers == 0:
                break

    df = pd.DataFrame(scraped_data)
    df.to_csv(f'irna-{year}.csv')

if __name__ == '__main__':
    scrap_year(1400)
