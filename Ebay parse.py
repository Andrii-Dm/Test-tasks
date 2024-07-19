import requests
from bs4 import BeautifulSoup
import json


class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.item = {}

    def fetch_page(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        return response.text

    def parse_page(self, page):

        soup = BeautifulSoup(page, 'html.parser')

        title = soup.find("h1", class_="x-item-title__mainTitle")
        self.item['title'] = title.text.strip() if title else 'N/A'

        img = soup.find("div", class_="ux-image-carousel-container image-container").find("img")
        self.item['image'] = img['src'] if img else 'N/A'

        condition = soup.find("div", class_="x-item-condition-text").find('span', class_="ux-textspans")
        self.item['condition'] = condition.text.strip() if condition else 'N/A'

        self.item['url'] = url

        cost = soup.find("div", class_="x-price-primary")
        self.item['cost'] = cost.text.strip() if cost else 'N/A'

        seller = soup.find("div", class_="x-sellercard-atf__info").find("span",
                                                                        class_="ux-textspans ux-textspans--BOLD")
        if not seller:
            seller = soup.find("div", class_="x-sellercard-atf__info").find("span", class_="ux-textspans")
        self.item['seller'] = seller.text.strip() if seller else 'N/A'

        shipping = soup.find("div", class_="vim d-shipping-minview mar-t-20").find("div",
                                                                                   class_="ux-labels-values__values"
                                                                                          "-content").find(
            "span", class_="ux-textspans ux-textspans--BOLD")
        if shipping is None:
            shipping = soup.find("div", class_="vim d-shipping-minview mar-t-20").find("div",
                                                                                       class_="ux-labels"
                                                                                              "-values__values-content").find(
                "span", class_="ux-textspans ux-textspans--BOLD ux-textspans--NEGATIVE")
        elif shipping is None:
            shipping = soup.find("div", class_="vim d-shipping-minview mar-t-20").find("div",
                                                                                       class_="ux-labels"
                                                                                              "-values__values-content").find(
                "span", class_="ux-textspans ux-textspans")
        self.item['shipping'] = shipping.text.strip()

    def save_data_to_file(self, filename='ebay_product_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.item, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")

    def display_data(self):
        print(json.dumps(self.item, ensure_ascii=False, indent=4))

    def scrape(self):
        page = self.fetch_page()
        if page:
            self.parse_page(page)
            self.save_data_to_file()
            self.display_data()


url = input("What are we scraping today?")
scraper = EbayScraper(url)
scraper.scrape()
