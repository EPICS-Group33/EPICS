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

        d1 = soup.find_all('div' , class_ = 'pannel_wrapper_container')
        for d2 in d1 :
            for ul in d2.find_all('ul', class_='a_z_listing'):
                ul.extract()
            for d3 in d2.find_all('li'):  
                '''print(f'{d3.a}')'''
                link = d3.a
                text = link.get_text()
                href = link['href']
                '''print(f'{text} link = { href }')'''
                writer.writerow([text, href])


Main_list_of_diseases("https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/")