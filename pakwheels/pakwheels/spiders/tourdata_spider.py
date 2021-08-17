import scrapy
from scrapy.http import HtmlResponse
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class TourDataSpider(scrapy.Spider):
    name = "tourspider"

    start_urls = [
        'https://findmyadventure.pk/trip/4565/trip-to-phandar-naltar-valley',
    ]

    def __init__(self):
        options = Options()
        # initiate webdriver in headless and incognito
        options.add_argument("--headless")
        options.add_argument("--incognito")
        chromedriver_path = (
            os.path.abspath(os.path.dirname(__name__))+'/chromedriver'
            )
        self.driver = webdriver.Chrome(chromedriver_path, options=options)

    def parse(self, response):
        """
        Parses response and scraps data

        Arguments:
            self
            response: Response object
        """

        self.driver.get(response.url)
        # max wait time for driver
        wait = WebDriverWait(self.driver, 5)
        try:
            # wait until fb-customer-chat is not loaded or wait upto 5 seconds
            wait.until(
                lambda driver: driver.find_element_by_id('fb-customer-chat')
                )
        finally:
            # click on book now button
            self.driver.find_element_by_id('book-now').click()
            # build scrapy response object from the page source
            response = HtmlResponse(
                url='', body=self.driver.page_source, encoding='UTF-8'
                )
            # scrap price and dates
            price = response.css('.modal-dialog .price::text').get()
            price = price.split()[1]
            dates = response.css(
                '.date-button-spacing.ng-star-inserted button::text'
                ).getall()
            data = [{'date':date, 'price':price} for date in dates]
            print(data)
