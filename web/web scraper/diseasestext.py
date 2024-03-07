import requests
from bs4 import BeautifulSoup

def work(link, output_file):
    # Fetch the HTML content from the link
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    # Open the output file
    with open(output_file, "w", encoding='utf-8') as file:
        d1 = soup.find_all('div', class_='pannel_wrapper_container')
        for d2 in d1:
            for ul in d2.find_all('ul', class_='a_z_listing'):
                ul.extract()
            for d3 in d2.find_all('li'):
                a_tag = d3.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    # Write the text and href of each <a> tag to the file
                    file.write(f"{a_tag.get_text()}: {a_tag['href']}\n")

   

# Example usage
work('https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/', 'output.txt')
