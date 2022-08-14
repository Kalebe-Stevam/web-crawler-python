import sys

import requests
from bs4 import BeautifulSoup


TO_CRAWL = []
CRAWLED = set()  # tipo uma lista, mas encontra o que tem dentro mais rapido


def request(url):
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
    try:
        response = requests.get(url, headers=header)
        return response.text
    
    except KeyboardInterrupt:
        sys.exit(0)  # pra conseguir dar ctrl c e sair 
    except:
        pass


def get_links(html):
    links = []
    try:
        soup = BeautifulSoup(html, "html.parser")  # faz o parser
        tags_a = soup.find_all("a", href=True)  # cria uma lista com a teg "a"/ filtra so as que tem href 
        for tag in tags_a:
            link = tag["href"]  # pega o href da teg
            if link.startswith("http"):
                links.append(link)
        return links
    except Exception as e:
        print("get_links Error: ", e)


def craw():
    while True:
        if TO_CRAWL:
            url = TO_CRAWL.pop()  # recebe e exclui o ultimo item da lista
            html = request(url)
            if html:
                links = get_links(html)
                if links:
                    for link in links:
                        if link not in CRAWLED and link not in TO_CRAWL:  # Verificando se não esta em nem uma lista 
                            TO_CRAWL.append(link)  # add in lista
                print(f"Crawling: {url}")
                CRAWLED.add(url)  # add in crawled
            else:
                CRAWLED .add(url)  # se o html tiver dado errado ele adiciona para não tentar denovo 

        else:
            print("done")
            break

if __name__ == "__main__":
    url = sys.argv[1]
    TO_CRAWL.append(url)
    craw()

