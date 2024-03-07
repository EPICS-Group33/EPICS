import requests
from bs4 import BeautifulSoup
import csv


def read_from_link(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    active_div = soup.find('div', class_='col-sm-12 illnessPart1')
    if active_div is not None:
        text = active_div.text.strip()
        print(text)
        return text
    else:
        print("Content not found for URL:", link)
        return "Content not found"
    

def read_links_and_write_content(input_csv_path, output_csv_path):
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        links = [row['Link'] for row in reader]
        

    rows = [{'Link': link, 'information': read_from_link(link)} for link in links]
    

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Link', 'information']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


input_csv_path = 'C:/Users/siddh/OneDrive/Desktop/C C++/links.csv'

output_csv_path = 'C:/Users/siddh/OneDrive/Desktop/C C++/information.csv'

read_links_and_write_content(input_csv_path, output_csv_path)


