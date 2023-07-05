import requests
from bs4 import BeautifulSoup
import sys


sys.stdout.reconfigure(encoding='utf-8')

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
pages_to_scrape = 20

products = []

for page in range(1, pages_to_scrape + 1):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_list = soup.find_all('div', {'class': 's-result-item'})
    for product in product_list:
        product_url_element = product.find('a', {'class': 'a-link-normal'})
        product_name_element = product.find('span', {'class': 'a-size-medium'})
        product_price_element = product.find('span', {'class': 'a-offscreen'})
        rating_element = product.find('span', {'class': 'a-icon-alt'})
        num_reviews_element = product.find('span', {'class': 'a-size-base'})
        
        if product_url_element is not None:
            product_url = product_url_element.get('href')
        else:
            product_url = ''
        
        if product_name_element is not None:
            product_name = product_name_element.text.strip()
        else:
            product_name = ''
        
        if product_price_element is not None:
            product_price = product_price_element.text.strip()
        else:
            product_price = ''
        
        if rating_element is not None:
            rating = rating_element.text.strip()
        else:
            rating = ''
        
        if num_reviews_element is not None:
            num_reviews = num_reviews_element.text.strip()
        else:
            num_reviews = ''
        
        product_data = {
            'url': product_url,
            'name': product_name,
            'price': product_price,
            'rating': rating,
            'num_reviews': num_reviews
        }
        
        products.append(product_data)

# Print the scraped product information
for product in products:
    print('Product Name:', product['name'])
    print('URL:', product['url'])
    print('Price:', product['price'])
    print('Rating:', product['rating'])
    print('Number of Reviews:', product['num_reviews'])

