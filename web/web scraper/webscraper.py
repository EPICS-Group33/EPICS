import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
url_to_scrape = "https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/"

# Send a GET request to the URL
response = requests.get(url_to_scrape)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main container 'div' element that has the class 'pannel_wrapper_container'
main_div = soup.find('div', class_='pannel_wrapper_container')

# Find all 'div' elements for each alphabetical section
alphabetical_divs = main_div.find_all('div', class_=lambda x: x and x.startswith('az_list_indivisual'))

# Open a CSV file for writing
with open('diseases.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Disease'])

    # Iterate over each alphabetical 'div' to find 'ul' elements within
    for div in alphabetical_divs:
        # Find the 'ul' element within the 'div'
        ul = div.find('ul')
        if ul:
            # Find all 'li' elements within the 'ul'
            lis = ul.find_all('li')
            for li in lis:
                # Extract the text and strip any extra whitespace
                disease_name = li.get_text().strip()
                # Write the disease name to the CSV file
                writer.writerow([disease_name])

print('Diseases have been written to diseases.csv')




file.close()    