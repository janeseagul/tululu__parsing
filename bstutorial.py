import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://tululu.org/b1/'

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('body').find('table').find('td', class_='ow_px_td').find('div').find('h1').text
title_tag = title_tag.split('   ::   ')
title_tag[0].strip()
title_tag[1].strip()
print(title_tag)

# url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
# response = requests.get(url)
# response.raise_for_status()
# soup = BeautifulSoup(response.text, 'lxml')
# title_tag = soup.find('main').find('header').find('h1')
# title_text = title_tag.text
# print(title_text)
# img_tag = soup.find('img', class_='attachment-post-image')['src']
# print(img_tag)
# post_tag = soup.find('div', class_='entry-content')
# post_text = post_tag.text
# print(post_text)