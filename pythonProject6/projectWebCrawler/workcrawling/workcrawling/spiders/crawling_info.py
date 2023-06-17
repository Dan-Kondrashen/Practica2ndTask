from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import logging
import datetime

##Наш паучек, собирающий данные с сайтов
class CrawlingInfo(CrawlSpider):
    # startDate = datetime.date(2023, 6, 12)
    # endDate = datetime.date.today()
    ##Это нужно если возникнет желание собирать данные по определенной дате
    dateToday = date.today().strftime("%Y/%m/%d")
    # datestep = datetime.timedelta(days=1)
    name = "prcrawler"
    allowed_domains = ["militaryleak.com", "www.govconwire.com"]
    start_urls = ["https://militaryleak.com/", "https://militaryleak.com/page/2",
                  "https://www.govconwire.com/category/contract_awards/"]

    # def __init__(self):
    #     self.driver = webdriver.Safari

    PROXY_SERVER = "8.219.97.248:80"

    rules = (
        ##Для определения конкретных ссылок и вызова функций сбора данных
        Rule(LinkExtractor(allow=r"\d+/\d+/\d+/"), callback="parse_1stSite"),
        Rule(LinkExtractor(allow=r"\d+/\d+/", deny='/militaryleak.com/'), callback="parse_2ndSite"),
    )
    logging.basicConfig(filename='resultSp.log', level=logging.DEBUG)

    ##Функция сбора данных с первого сайта
    def parse_1stSite(self, response):
        self.logger.info("Parse function called on %s", response.url)
        yield {
            "title": response.css(".entry-title::text").get(),
            "date": response.css(".posted-on time::text").get(),
            "author": response.css(".entry-author span::text").get(),
            "content": response.css(".entry-content p::text").getall(),
            "hyperlink": response.url
        }
    ##Функция сбора данных со второго сайта
    def parse_2ndSite(self, response):
        # self.driver.get(response.url)
        # actions = ActionChains(self.driver)
        # actions.send_keys(Keys.PAGE_DOWN).perform()
        # popup_close_button = WebDriverWait(self.driver, 3).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".ays_pb_material_close_circle_icon"))
        # )
        # popup_close_button.click()
        # content = response.css(".entry-content p span::text").getall(),
        # contentFiltr = [item.replace("', '", " ") for item in content]
        yield {
            "title": response.css(".entry-title::text").get(),
            "date": response.css(".post-date a::text").get(),
            "author": response.css(".author-name::text").get(),
            "content": response.css(".entry-content p span::text").getall(),
            "hyperlink": response.url
        }
