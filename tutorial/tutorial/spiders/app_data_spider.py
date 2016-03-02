from scrapy.spiders import Spider
from scrapy.selector import Selector
from tutorial.items import TutorialItem
from bs4 import BeautifulSoup
import requests


class Books_and_Reference(Spider):
    name = 'books_and_reference'  
    allowed_domains = ["play.google.com"]
    start_urls = ['https://play.google.com/store/apps/category/BOOKS_AND_REFERENCE/collection/topselling_paid']

    def parse(self,response):
            sel    = Selector(response)
            titles = sel.xpath('//div[@class = "details"]/a[@class = "title"]')
            for title in titles :
                      item = TutorialItem()
                      item["title"] = title.select("text()").extract()
                      item["link"] = 'https://play.google.com'+title.select("@href").extract()[0]
                      r = requests.get(item["link"])
                      data = r.text
                      soup = BeautifulSoup(data)
                      letters = soup.find_all("div", class_="review-body")
                      reviewMap = []
                      for element in letters:
                        reviewMap.append(element.get_text()+"\n")
                      item["reviews"] = reviewMap
                      yield item
