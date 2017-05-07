from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

baseUrl = 'https://www.yelp.com/search?find_loc=Eden+Prairie,+MN&start=0&cflt=restaurants'
baseUrl_html = urlopen(baseUrl)
baseUrl_Obj = BeautifulSoup(baseUrl_html)

num_of_pages = int(re.findall('^.*\s([0-9]+)$',
                              baseUrl_Obj.find('div', {
                                  'class': 'page-of-pages arrange_unit arrange_unit--fill'}).text.strip())[0])

for RestHref in baseUrl_Obj.find_all('li', {'class': 'regular-search-result'}):
    RestUrl = 'www.yelp.com' + RestHref.find('a', {'class': 'biz-name js-analytics-click'}).attrs['href']
    PhotoUrl = 'www.yelp.com' + RestHref.find('a', {'class': 'biz-name js-analytics-click'}).attrs['href'].replace(
        'biz', 'biz_photos') + '?tab=food'
    RestUrl_html = urlopen('https://' + RestUrl)
    RestUrl_Obj = BeautifulSoup(RestUrl_html)

    if RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}) is None:
        rating = -1.0
    else:
        rating =int(re.findall('^\s+([0-9]+)\s.*', RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}).div.span.text)[0])
    print(rating)

        re.findall('^\s+([0-9]+)\s.*$',
def YelpSpider(baseUrl):
    baseUrl = 'https://www.yelp.com/search?find_loc=Eden+Prairie,+MN&start=0&cflt=restaurants'
    baseUrl_html = urlopen(baseUrl)
    baseUrl_Obj = BeautifulSoup(baseUrl_html)

    num_of_pages = int(re.findall('^.*\s([0-9]+)$',
                                  baseUrl_Obj.find('div', {
                                      'class': 'page-of-pages arrange_unit arrange_unit--fill'}).text.strip())[0])

    for page_num in range(0, num_of_pages):
        SearchUrl = 'https://www.yelp.com/search?find_loc=Eden+Prairie,+MN&start={}&cflt=restaurants'.format(
            page_num * 10)
        SearchUrl_html = urlopen(SearchUrl)
        SearchUrl_Obj = BeautifulSoup(SearchUrl_html)

        for RestHref in SearchUrl_Obj.find_all('li', {'class': 'regular-search-result'}):
            RestUrl = 'www.yelp.com' + RestHref.find('a', {'class': 'biz-name js-analytics-click'}).attrs['href']
            RestUrl_html = urlopen(RestUrl)
            RestUrl_Obj = BeautifulSoup(RestUrl_html)

            if RestUrl_Obj.find('h1', {'class': 'biz-page-title embossed-text-white shortenough'}) is None:
                RestName = RestUrl_Obj.find('h1', {'class': 'biz-page-title embossed-text-white'}).text
            else:
                RestName = RestUrl_Obj.find('h1', {'class': 'biz-page-title embossed-text-white shortenough'}).text

            if RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}) is None:
                rating = -1.0
                num_of_reviews = 0
            else:
                rating = float(
                    re.findall('\d+\.\d+', RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}).div.div['title'])[
                        0])
                num_of_reviews = int(re.findall('^\s+([0-9]+)\s.*',
                                        RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}).div.span.text)[0])



            PhotoUrl = 'www.yelp.com' + RestHref.find('a', {'class': 'biz-name js-analytics-click'}).attrs[
                'href'].replace(
                'biz', 'biz_photos') + '?tab=food'
            print(RestName)
