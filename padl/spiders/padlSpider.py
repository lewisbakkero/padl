# -*- coding: utf-8 -*-
import scrapy
from padl.items import AmazonItem
import os
import re
import logging
from logging.config import fileConfig

class padlSpider(scrapy.Spider):
    imgcount = 1
    name = "amazon"
    allowed_domains = ["amazon.com"]

    def __init__(self, credentialsFile= None):
        thisDir = os.path.abspath(os.path.dirname(__file__))
        logConfigFile = os.path.join(thisDir, 'config', 'logging_config.ini')
        self.setup_logger(logConfigFile)

    def setup_logger(self, logConfigFile):
        fileConfig(logConfigFile)
        self.logger = logging.getLogger(__name__)


    '''
    start_urls = ["http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=backpack",
                  "http://www.amazon.com/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Abackpack&page=2&keywords=backpack&ie=UTF8&qid=1442907452&spIA=B00YCRMZXW,B010HWLMMA"
                  ]
    '''
    def start_requests(self):
        yield scrapy.Request("http://www.amazon.com/s/ref=sr_ex_n_3?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A9479199011%2Cn%3A360832011&bbn=10445813011&ie=UTF8&qid=1442910853&ajr=0",self.parse)
        
        for i in range(2,3):
            yield scrapy.Request("http://www.amazon.com/s/ref=lp_360832011_pg_2?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A9479199011%2Cn%3A360832011&page="+str(i)+"&bbn=10445813011&ie=UTF8&qid=1442910987",self.parse)
        
    
    
    def parse(self,response):
        #namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@title').extract()
        #htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href').extract()
        #imglist = response.xpath('//a[@class="a-link-normal a-text-normal"]/img/@src').extract()
        #namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"]/@title').extract()
        #htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"]/@href').extract()
        #imglist = response.xpath('//img[@class="s-access-image cfMarker"]/@src').extract()

        self.logger.debug()
        asins = response.xpath('//li[contains(.,"ASIN: ")]//text()').extract()
        text = str(response.xpath('//text()').extract()).replace('\n', ' ')
        prices = re.search(ur'([£\$€])(\d+(?:\.\d{2})?)', text).groups() #response.xpath('//table[contains(@class,"a-lineitem")]//span[@id="priceblock_ourprice"]//text()').extract()
        listlength = len(asins)
        priceslength = len(prices)
        
        pwd = os.getcwd()+'/'

        if not os.path.isdir(pwd+'crawlImages/'):
            os.mkdir(pwd+'crawlImages/')

        for i in range(0,listlength):
            item = AmazonItem()
            self.logger.debug(i+" "+str(item))
            yield item



    def setup_logger(self, logConfigFile):
        fileConfig(logConfigFile)
        self.logger = logging.getLogger(__name__)