import requests
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
import lxml


def download_txt(url, filename, number, folder='Books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    Path(f'./{folder}').mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = Path(f'./{folder}/{number}.{filename}.txt')

    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def fetch_book_title(page_url):
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('body').find('table').find('td', class_='ow_px_td').find('div').find('h1').text
    title_tag = title_tag.split('   ::   ')

    title_tag[0].strip()
    title_tag[1].strip()
    return title_tag[0]


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    for book_id in range(1, 11):
        try:
            url_pattern = f'https://tululu.org/txt.php?id={book_id}'
            page_url = f'https://tululu.org/b{book_id}'
            filename = fetch_book_title(page_url)

            download_txt(url_pattern, filename, book_id)
        except requests.exceptions.HTTPError:
            print(f"Can't create book {filename}, it does not exist!")
        except IndexError:
            print(f"Can't create book {filename}, it does not exist!")


if __name__ == '__main__':
    main()
