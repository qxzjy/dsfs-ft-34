import os
import logging
import argparse
import scrapy
from scrapy.crawler import CrawlerProcess

urls_list = []
base_url = "https://www.booking.com/searchresults.fr.html?ss="


# parser = argparse.ArgumentParser()

# for i in range(5):
#     parser.add_argument('--city_'+str(i+1), dest='city_'+str(i+1), type=str, help='Add city_'+str(i+1))

# args = parser.parse_args()

# urls_list.append(base_url+args.city_1)
# urls_list.append(base_url+args.city_2)
# urls_list.append(base_url+args.city_3)
# urls_list.append(base_url+args.city_4)
# urls_list.append(base_url+args.city_5)

class BookingSpider(scrapy.Spider):

    name = "booking"

    # start_urls = [
    #      "https://www.booking.com/searchresults.fr.html?ss=Paris",
    #      "https://www.booking.com/searchresults.fr.html?ss=Rouen"
    # ]

    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"
    }

    def start_requests(self):
        urls = load_urls()
        
        for index, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse, meta={"city_id":index+1}) 

    def parse(self, response):
        hotels = response.xpath('/html/body/div[4]/div/div/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[@data-testid="property-card"]')

        for hotel in hotels:

            url = hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a[@data-testid="title-link"]/@href').get()

            yield scrapy.Request(url=url, callback=self.parse_hotel_details, meta={"city_id":response.meta["city_id"]})
        

    def parse_hotel_details(self, response):
            
            coordinates = response.xpath('//*[@id="map_trigger_header_pin"]/@data-atlas-latlng').get()

            latitude = coordinates.split(",")[0]
            longitude = coordinates.split(",")[1]

            yield {
                'name': response.xpath('//*[@id="hp_hotel_name"]/div/h2/text()').get(),
                'rating': response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div[1]/text()').get(),
                'lat': latitude,
                'lon': longitude,
                'description': response.xpath('//*[@id="basiclayout"]//*[@data-testid="property-description"]/text()').get(),
                'url': response.url,
                'city_id': response.meta["city_id"]
            }
            
# Name of the file where the results will be saved
filename = "hotels.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('data/'):
        os.remove('data/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'data/' + filename: {"format": "json"},
    }
})

def load_urls():

    base_url = "https://www.booking.com/searchresults.fr.html?ss="

    cities_list = ["Mont Saint Michel",
                    "St Malo",
                    "Bayeux",
                    "Le Havre",
                    "Rouen",
                    "Paris",
                    "Amiens",
                    "Lille",
                    "Strasbourg",
                    "Chateau du Haut Koenigsbourg",
                    "Colmar",
                    "Eguisheim",
                    "Besancon",
                    "Dijon",
                    "Annecy",
                    "Grenoble",
                    "Lyon",
                    "Gorges du Verdon",
                    "Bormes les Mimosas",
                    "Cassis",
                    "Marseille",
                    "Aix en Provence",
                    "Avignon",
                    "Uzes",
                    "Nimes",
                    "Aigues Mortes",
                    "Saintes Maries de la mer",
                    "Collioure",
                    "Carcassonne",
                    "Ariege",
                    "Toulouse",
                    "Montauban",
                    "Biarritz",
                    "Bayonne",
                    "La Rochelle"]
    
    urls = [base_url+i for i in cities_list]

    return urls
     
# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()