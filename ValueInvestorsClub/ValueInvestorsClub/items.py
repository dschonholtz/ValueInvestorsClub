# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
"""
This is a file that when given a link, it will go to that link and collect the following information:

Ticker: The ticker symbol of the company
Company Name: The name of the company
Date: The datetime the idea was posted
Author: The name of the author of the idea
Short: bool - If the writer is short. Assumed long if not short.
IsContestWinner: bool
Description:
Catalyst:

Later we will pull the following equity information from various API's.
Price At the writing of the article
Price1Mo The price 1 month out
Price3Mo The price 3 months out
Price6Mo The price 6 months out
Price1Yr The price 1 year out
Price2Yr The price 2 years out
Price3Yr The price 3 years out
Price5Yr The price 5 years out
"""

import scrapy


class ValueinvestorsclubItem(scrapy.Item):
    
    link = scrapy.Field()
    # This is the ticker symbol of the company
    ticker = scrapy.Field()
    # This is the name of the company
    companyName = scrapy.Field()
    # This is the date the idea was posted
    date = scrapy.Field()
    # This is the name of the author of the idea
    username = scrapy.Field()
    userLink = scrapy.Field()
    
    # This is the short bool
    isShort = scrapy.Field()
    
    # This is the isContestWinner bool
    isContestWinner = scrapy.Field()
    
    # This is the description of the idea
    description = scrapy.Field()
    
    # This is the catalyst of the idea
    catalysts = scrapy.Field()
    
    # This is the price at the time of the article
    price = scrapy.Field()
    
    # This is the price 1 month out
    price1Mo = scrapy.Field()
    
    # This is the price 3 months out
    price3Mo = scrapy.Field()
    
    # This is the price 6 months out
    price6Mo = scrapy.Field()
    
    # This is the price 1 year out
    price1Yr = scrapy.Field()
    
    # This is the price 2 years out
    price2Yr = scrapy.Field()
    
    # This is the price 3 years out
    price3Yr = scrapy.Field()
    
    # This is the price 5 years out
    price5Yr = scrapy.Field()

    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({"link": str(self["link"])})
