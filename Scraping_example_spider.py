import scrapy

#class for scraping
class SunzelSpider(scrapy.Spider):
    #name of the spider
    name = 'Sunzel'

    allowed_domains = ['amazon.com']

    # Base URL for Sunzel
    myBaseUrl = "https://www.amazon.com/Fulfillment-Sunzel-Shields-Sponges-Protect/product-reviews/B08K2Q9MD3/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls=[]
 
    # Creating list of urls to be scraped by appending page number at the end of base url
    for i in range(1,150):
        start_urls.append(myBaseUrl+str(i))
 
    # Defining a Scrapy parser
    def parse(self, response):
            #grabbing the list of reviews object from the websites (refering to the css code of the website)
            data = response.css('#cm_cr-review_list')

            #grabbing each review on the list with all the information
            reviews = data.css('.review')

            #empty lists for all the information we are extracting
            title=[]
            date_posted=[]
            star_rating=[]
            comment=[]
            useful_vote=[]
            count=0 #counter
            #looping through each review
            for review in reviews:
                #grabbing the sections from the reviews we want to extract
                title = reviews[count].css('.review-title')
                date_posted = reviews[count].css('.review-date')
                star_rating = reviews[count].css('.review-rating')
                comment = reviews[count].css('.review-text')
                useful_vote = reviews[count].css('.cr-vote-text') if reviews[count].css('.cr-vote-text') else '0' #grabbing if helpful vote num. exists otherwise 0
                #extracting data into a dictionary
                yield{'title' : ''.join(title.xpath('.//text()').extract()),
                      'date_posted' : ''.join(date_posted.xpath('.//text()').extract()),
                      'star_rating' : ''.join(star_rating.xpath('.//text()').extract()),
                      'comment' : ''.join(comment.xpath('.//text()').extract()),
                      'usefulness' : ''.join(useful_vote) if useful_vote=='0' else ''.join(useful_vote.xpath('.//text()').extract())} #if it exists extract, if not 0
                
                count=count+1

