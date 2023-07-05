import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'
pages_to_scrape = 40

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
            product_url = urljoin(base_url, product_url)  # Construct the absolute URL
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

# Scrape information from product URLs
for product in products:
    url = product['url']

    if url == '':
        continue  

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    description_element = soup.find('div', {'id': 'feature-bullets'})
    asin_element = soup.find('th', text='ASIN')
    product_description_element = soup.find('div', {'id': 'productDescription'})
    manufacturer_element = soup.find('a', {'id': 'bylineInfo'})

    if description_element is not None:
        description = description_element.text.strip()
    else:
        description = ''

    if asin_element is not None:
        asin = asin_element.find_next('td').text.strip()
    else:
        asin = ''

    if product_description_element is not None:
        product_description = product_description_element.text.strip()
    else:
        product_description = ''

    if manufacturer_element is not None:
        manufacturer = manufacturer_element.text.strip()
    else:
        manufacturer = ''


    product['description'] = description
    product['asin'] = asin
    product['product_description'] = product_description
    product['manufacturer'] = manufacturer

# Export the data to a CSV file
filename = 'scrape_data.csv'
fields = ['name', 'url', 'price', 'rating', 'num_reviews', 'description', 'asin', 'product_description', 'manufacturer']

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(products)

print('Data has been exported to', filename)
