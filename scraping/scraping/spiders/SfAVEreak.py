# Importing Scrapy Library
import scrapy
import re
 
# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
 
    # Spider name
    name = 'SfAVEreak'
 
    # Domain names to scrape
    allowed_domains = ['amazon.com']
 
    # Base URL for the MacBook air reviews
    myBaseUrl = "https://www.amazon.com/SfAVEreak-Face-Disposable-Pollution-Protection/product-reviews/B08725VTGK/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls=[]
 
    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1,86):
        start_urls.append(myBaseUrl+str(i))
 
    # Defining a Scrapy parser
    def parse(self, response):
            data = response.css('#cm_cr-review_list')

            reviews = data.css('.review')

            title=[]
            date_posted=[]
            star_rating=[]
            comment=[]
            useful_vote=[]
            count=0
            for review in reviews:
                title = reviews[count].css('.review-title')
                date_posted = reviews[count].css('.review-date')
                star_rating = reviews[count].css('.review-rating')
                comment = reviews[count].css('.review-text')
                useful_vote = reviews[count].css('.cr-vote-text') if reviews[count].css('.cr-vote-text') else '0'

                yield{'title' : ''.join(title.xpath('.//text()').extract()),
                      'date_posted' : ''.join(date_posted.xpath('.//text()').extract()),
                      'star_rating' : ''.join(star_rating.xpath('.//text()').extract()),
                      'comment' : ''.join(comment.xpath('.//text()').extract()),
                      'usefulness' : ''.join(useful_vote) if useful_vote=='0' else ''.join(useful_vote.xpath('.//text()').extract())}
                
                count=count+1