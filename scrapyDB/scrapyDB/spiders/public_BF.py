import scrapy
import re
from urllib.parse import urlencode

from scrapyDB.items import publicItems

# from scrapyDB.items import publicItems  

API_KEY = '91429597-550a-431f-949d-0a156f5e12b1'  # Replace with your ScrapeOps API key

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'bypass': 'cloudflare'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

def clean_price(price_str):
    if not price_str:
        return None
    price_str = price_str.replace('€', '')
    price_str = price_str.replace(',', '.')
    price_str = re.sub(r'\s+', '', price_str)  # Remove all whitespace
    try:
        return float(price_str)
    except ValueError:
        return None


class PublicScrapy(scrapy.Spider):
    name = "public_BF"
    page_number = 1  # Initialize page number

    def start_requests(self):
        categories = 'scrapyDB\spiders\public_categories.txt'
        with open(categories, 'r') as file:
            urls = [url.strip() for url in file.readlines()]

        for url in urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)
        

    def parse(self, response):
        for product in response.css('.product-tile-container'):
            product_link = product.css('.mdc-link-button.animate.mdc-link-button--black.mdc-link-button--clamp.text-left.mdc-link-button--semibold::attr(href)').get()
            if product_link:
                product_link = response.urljoin(product_link)
                product_link = product_link.replace('https://proxy.scrapeops.io', 'https://www.public.gr')

            name = product.css('.mdc-link-button__label--clamp--2.mdc-link-button__label-tile-list--clamp--2.mdc-typography--headline7.mdc-link-button__label::text').get()
            category = response.css('.header-section h1::text').get()
            started_price_main = product.css('.product__price--line-through::text').get()
            started_price_decimal = product.css('.product__price--line-through + sup::text').get()
            discounted_amount_main = product.css('.product__price--discount > span > span::text').get()
            discounted_amount_decimal = product.css('.product__price--discount sup::text').get()
            current_price_main = product.xpath('.//div[contains(@class, "product__price--final")]/app-product-price/div/text()').get()
            current_price_decimal = product.css('.product__price--final sup::text').get()

            # Safely concatenate price components, handling None values
            started_price = clean_price((started_price_main or '') + (started_price_decimal or ''))
            current_price = clean_price((current_price_main or '') + (current_price_decimal or ''))
            discounted_amount = clean_price((discounted_amount_main or '') + (discounted_amount_decimal or ''))


            discount_percentage_calculated = calculate_discount_percentage(started_price, current_price)

            item = publicItems()

            item['name'] = name
            item['category'] = category
            item['started_price'] = started_price
            item['current_price'] = current_price
            item['discounted_amount'] = discounted_amount
            item['discount_percentage'] = discount_percentage_calculated
            item['product_link'] = product_link

            yield item

def calculate_discount_percentage(started_price, current_price):
    if started_price is None or current_price is None:
        return None

    if started_price <= 0:
        return None

    discount_percentage = ((started_price - current_price) / started_price) * 100
    return round(discount_percentage, 2)  # rounding to 2 decimal places
