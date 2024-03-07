import requests
from bs4 import BeautifulSoup
import csv


"""def read_from_link(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')"""

def Main_list_of_diseases(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')

    with open('links.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Text', 'Link'])

        disease_container = soup.find_all('div' , class_ = 'pannel_wrapper_container')

        for disease_lists in disease_container :

            for unwanted_lists in disease_lists.find_all('ul', class_='a_z_listing'):
                unwanted_lists.extract()

            for wanted_lists in disease_lists.find_all('li'):  
                link = wanted_lists.a
                text = link.get_text()
                href = link['href']

                writer.writerow([text, href])


Main_list_of_diseases("https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/")