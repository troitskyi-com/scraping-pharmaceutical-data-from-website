import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://epharma.com.bd/en/medicines'

# Get the HTML
request = requests.get(url)

#print status code with message "status code: "
print("status code:", request.status_code)

# Parse the HTML
soup = BeautifulSoup(request.text, 'html.parser')

#find all the divs with class name 'col-md-2 p-0'
divs = soup.find_all('div', {'class': 'col-md-2 p-0'})

#put those in a list
divs_list = list(divs)

#add the next page to the list and loop through the list until you hit page 5
for i in range(2,6):
    url = 'https://epharma.com.bd/en/medicines?page=' + str(i)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    divs = soup.find_all('div', {'class': 'col-md-2 p-0'})
    divs_list.extend(divs)

#print the number of divs found
print("divs parsed:",len(divs_list))

#save the output to a sqlite database
import sqlite3
conn = sqlite3.connect('epharma.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS epharma
                (img_src text, name text, price text, link_href text)''')

# Insert a row of data
for div in divs_list:
    img = div.find('img', {'class': 'style__image___Ny-Sa style__loaded___22epL wow zoomIn'})
    name = div.find('div', {'class': 'style__name___3YOZc style__large-font___2dBUf'})
    price = div.find('div', {'class': 'style__price___196ew'})
    thumbnail_div = div.find('div', {'class': 'ps-product__thumbnail'})
    link = thumbnail_div.find('a') if thumbnail_div else None

    img_src = img['src'] if img else None
    name_text = name.text.strip() if name else None
    price_text = price.text.strip() if price else None
    link_href = link['href'] if link else None

    c.execute("INSERT INTO epharma VALUES (?,?,?,?)", (img_src, name_text, price_text, link_href))

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

