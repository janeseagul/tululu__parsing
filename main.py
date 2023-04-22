import requests
from pathlib import Path


def download_books(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'w') as file:
        file.write(response.text)


dir_name = 'Books'

for book_id in range(1, 11):
    link = f'https://tululu.org/txt.php?id={book_id}'
    filename = Path(f'./{dir_name}/{book_id}.txt')
    download_books(link, filename)
