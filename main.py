import requests
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
import lxml
from urllib.parse import unquote, urljoin, urlparse


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


def download_book_cover(cover_url, folder='Images/'):
    Path(f'./{folder}').mkdir(exist_ok=True)

    filename = unquote(urlparse(cover_url)).path.split('/')[-1]
    filename = sanitize_filename(filename)
    filepath = Path(f'./{folder}/{filename}')
    response = requests.get(cover_url)
    response.raise_for_status()

    check_for_redirect(response)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def parse_book_page(page_url):
    response = requests.get(page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('body').find('table').find('td', class_='ow_px_td').find('div').find('h1').text
    img_tag = soup.find('div', class_='bookimage').find('img')['src']
    comments = soup.find_all('div', class_='texts')
    comments_tag = [tag.find('span').text for tag in comments]
    genres = soup.find('span', class_='d_book').find_all('a')
    genres_tag = [tag.text for tag in genres]

    title_tag = title_tag.split('   ::   ')
    book_title = title_tag[0].strip()
    book_author = title_tag[1].strip()

    return book_title, img_tag, '\n'.join(comments_tag), genres_tag


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def main():
    site_link = 'https://tululu.org/'
    for book_id in range(1, 11):
        try:
            url_pattern = urljoin(site_link, f'txt.php?=id={book_id}')
            page_url = urljoin(site_link, f'/b{book_id}')
            filename, cover_url, book_comments, book_genres = parse_book_page(page_url)
            cover_url = urljoin(site_link, cover_url)

            download_txt(url_pattern, filename, book_id)
            download_book_cover(cover_url)
        except requests.exceptions.HTTPError:
            print(f"Can't create book {filename}, it does not exist!")
        except IndexError:
            print(f"Can't create book {filename}, it does not exist!")
        except AttributeError:
            print(f"Can't create book {filename}, it does not exist!")


if __name__ == '__main__':
    main()
