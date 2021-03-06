import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import os
import es
from parse import parse

visitedPage = []


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:

    def __init__(self, urls=[], limitPG=1):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.crawledPg = 0
        self.wantedPg = limitPG

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.get_text())
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        htmlFile = url.replace(
            'https://', '').replace('.', '_').replace('/', '_')
        if htmlFile[-1] == '_':
            htmlFile = htmlFile[:-1]
            # print(htmlFile)
        # Check duplicated pages:
        if url in visitedPage:
            print('Duplicated page found! Skipping this round ... ...\n')
            return True

        visitedPage.append(url)
        htmlFile += '.html'
        html = self.download_url(url)

        ESList = parse(url, html)
        print(url)
        es.uploadDoc(ESList)

        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

        htmlOutput = open('html/'+htmlFile, 'w', encoding='utf-8')
        htmlOutput.write(html)
        htmlOutput.close()
        self.visited_urls.append(url)
        return False

    def run(self):
        while self.urls_to_visit:
            isDuplicated = False
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            if self.crawledPg == self.wantedPg:
                print('\nCrawling finished!\n')
                break
            try:
                isDuplicated = self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                if isDuplicated == False:
                    self.crawledPg += 1


def crawler(url, pages):
    crw = Crawler(url, pages).run()
    hist = open('history.txt', 'w')
    for URLS in visitedPage:
        hist.write(URLS)
        hist.write('\n')
    hist.close()
