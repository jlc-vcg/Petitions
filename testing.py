# Finds the text paragraphs from the G4G website page.

import requests
from bs4 import BeautifulSoup

response = requests.get('https://example.com/')

print(response.status_code)
soup = BeautifulSoup(response.content, 'html.parser')

content_div = soup.find('div', class_='article--viewer_content')
if content_div:
    for para in content_div.find_all('p'):
        print(para.text.strip())
else:
    print("No article content found.")

# Open a text file in write mode
#with open("output.txt", "w") as file:
#    # Write the variable to the file
#    file.write(str(soup.prettify()))