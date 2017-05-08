from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

baseUrl = 'https://www.yelp.com/search?find_loc=Eden+Prairie,+MN&start=0&cflt=restaurants'


def YelpSpider(baseUrl):
    baseUrl_html = urlopen(baseUrl)
    baseUrl_Obj = BeautifulSoup(baseUrl_html)

    num_of_pages = int(re.findall('^.*\s([0-9]+)$',
                                  baseUrl_Obj.find('div', {
                                      'class': 'page-of-pages arrange_unit arrange_unit--fill'}).text.strip())[0])
    YelpRestaurant = {}

    for page_num in range(0, num_of_pages):
        SearchUrl = 'https://www.yelp.com/search?find_loc=Eden+Prairie,+MN&start={}&cflt=restaurants'.format(
            page_num * 10)
        SearchUrl_html = urlopen(SearchUrl)
        SearchUrl_Obj = BeautifulSoup(SearchUrl_html)

        for RestHref in SearchUrl_Obj.find_all('li', {'class': 'regular-search-result'}):
            RestUrl = 'www.yelp.com' + RestHref.find('a', {'class': 'biz-name js-analytics-click'}).attrs['href']
            RestUrl_html = urlopen('https://' + RestUrl)
            RestUrl_Obj = BeautifulSoup(RestUrl_html)

            if RestUrl_Obj.find('h1', {'class': 'biz-page-title embossed-text-white shortenough'}) is None:
                RestName = RestUrl_Obj.find('h1', {'class': 'biz-page-title embossed-text-white'}).text.strip()
            else:
                RestName = RestUrl_Obj.find('h1',
                                            {'class': 'biz-page-title embossed-text-white shortenough'}).text.strip()

            if RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}) is None:
                rating = -1.0
                num_of_reviews = 0
            else:
                rating = float(
                    re.findall('\d+\.\d+', RestUrl_Obj.find('div', {'class': 'rating-info clearfix'}).div.div['title'])[
                        0])
                num_of_reviews = int(re.findall('^\s+([0-9]+)\s.*',
                                                RestUrl_Obj.find('div',
                                                                 {'class': 'rating-info clearfix'}).div.span.text)[0])

            if RestUrl_Obj.find('div', {'class': 'map-box-address u-space-l4'}).strong.address is None:
                address_1 = 'Unknown'
                address_2 = 'Unknown'
            elif len(RestUrl_Obj.find('div', {'class': 'map-box-address u-space-l4'}).strong.address.contents) == 3:
                address_1 = RestUrl_Obj.find('div', {'class': 'map-box-address u-space-l4'}).strong.address.contents[
                    0].strip()
                address_2 = RestUrl_Obj.find('div', {'class': 'map-box-address u-space-l4'}).strong.address.contents[
                    2].strip()
            else:
                address_1 = RestUrl_Obj.find('div', {'class': 'map-box-address u-space-l4'}).strong.address.contents[
                    0].strip()
                address_2 = 'Unknown'

            if RestUrl_Obj.find('span', {'class': 'biz-phone'}) is None:
                phone = 9999999999
            else:
                phone = int(''.join(re.findall('\d+', RestUrl_Obj.find('span', {'class': 'biz-phone'}).text)))

            if RestUrl_Obj.find('span', {'class': 'category-str-list'}).a is None:
                category = 'Unknown'
            else:
                category = RestUrl_Obj.find('span', {'class': 'category-str-list'}).a.text

            if RestUrl_Obj.find('span', {'class': 'business-attribute price-range'}) is None:
                price_range = -1
            else:
                price_range = len(RestUrl_Obj.find('span', {'class': 'business-attribute price-range'}).text)

            PhotoUrl = 'www.yelp.com' + RestHref.find('a', {'class': 'biz-name js-analytics-click'}).attrs[
                'href'].replace(
                'biz', 'biz_photos') + '?tab=food'

            YelpRestaurant[RestName] = [rating, num_of_reviews, address_1, address_2,
                                        phone, category, price_range]
    return YelpRestaurant


def YelpSpiderBasic(baseUrl):
    baseUrl_html = urlopen(baseUrl)
    baseUrl_Obj = BeautifulSoup(baseUrl_html)

    num_of_pages = int(re.findall('^.*\s([0-9]+)$',
                                  baseUrl_Obj.find('div', {
                                      'class': 'page-of-pages arrange_unit arrange_unit--fill'}).text.strip())[0])
    YelpRestaurant = {}

    for page_num in range(0, num_of_pages):
        SearchUrl = 'https://www.yelp.com/search?find_loc=Eden+Prairie,+MN&start={}&cflt=restaurants'.format(
            page_num * 10)
        SearchUrl_html = urlopen(SearchUrl)
        SearchUrl_Obj = BeautifulSoup(SearchUrl_html)

        for RestInfo in SearchUrl_Obj.find_all('li', {'class': 'regular-search-result'}):
            if RestInfo.find('a', {'class': 'biz-name js-analytics-click'}).span is not None:
                RestName = RestInfo.find('a', {'class': 'biz-name js-analytics-click'}).span.text
            else:
                RestName = 'Unknown'

            if RestInfo.find('div', {'class': 'biz-rating biz-rating-large clearfix'}) is None:
                rating = -1.0
                num_of_reviews = 0
            else:
                rating = float(re.findall('\d+\.\d+',
                                          RestInfo.find('div',
                                                        {'class': 'biz-rating biz-rating-large clearfix'}).div.attrs[
                                              'title'])[0])
                num_of_reviews = int(re.findall('^\s+([0-9]+)\s.*',
                                                RestInfo.find('div', {
                                                    'class': 'biz-rating biz-rating-large clearfix'}).span.text)[0])

            if RestInfo.find('div', {'class': 'secondary-attributes'}).address is None:
                address_1 = 'Unknown'
                address_2 = 'Unknown'
            elif len(RestInfo.find('div', {'class': 'secondary-attributes'}).address.contents) == 3:
                address_1 = RestInfo.find('div', {'class': 'secondary-attributes'}).address.contents[0].strip()
                address_2 = RestInfo.find('div', {'class': 'secondary-attributes'}).address.contents[2].strip()
            else:
                address_1 = RestInfo.find('div', {'class': 'secondary-attributes'}).address.contents[0].strip()
                address_2 = 'Unknown'

            if RestInfo.find('span', {'class': 'biz-phone'}).text is None or len(
                    RestInfo.find('span', {'class': 'biz-phone'}).text.strip()) == 0:
                phone = 9999999999
            else:
                phone = int(''.join(re.findall('\d+', RestInfo.find('span', {'class': 'biz-phone'}).text)))

            if RestInfo.find('span', {'class': 'category-str-list'}).a is None:
                category = 'Unknown'
            else:
                category = RestInfo.find('span', {'class': 'category-str-list'}).a.text

            if RestInfo.find('span', {'class': 'business-attribute price-range'}) is None:
                price_range = -1
            else:
                price_range = len(RestInfo.find('span', {'class': 'business-attribute price-range'}).text)

            YelpRestaurant[RestName] = [rating, num_of_reviews, address_1, address_2,
                                        phone, category, price_range]

            Yelp_df = pd.DataFrame.from_dict(YelpRestaurant, orient='index').rename(columns={0: 'rating',
                                                                                             1: 'num_of_reviews',
                                                                                             2: 'address_1',
                                                                                             3: 'address_2',
                                                                                             4: 'phone',
                                                                                             5: 'category',
                                                                                             6: 'price_range'})
    return Yelp_df
