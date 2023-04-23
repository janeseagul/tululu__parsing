from time import sleep
import sys
import requests
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse


def get_book_page(book_id):
    site = 'https://tululu.org/'
    url = urljoin(site, f'b{book_id}/')

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    return response


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def make_parser():
    parser = argparse.ArgumentParser(description='Скрипт для скачивания книг с сайта tululu.org ')
    parser.add_argument('start_index', help='С какого книги нужно начать скачивание', type=int)
    parser.add_argument('end_index', help='Какой книгой нужно завершить скачивание', type=int)
    return parser


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('h1')
    book_title, author = title_tag.text.split('::')
    book_title = book_title.strip()

    cover_image = soup.find('div', class_='bookimage').find('img')
    cover_image_url = urljoin(response.url, cover_image['src'])

    comments_tag = soup.find_all('div', class_='texts')
    comments = '\n'.join([tag.find('span').text for tag in comments_tag])

    book_genre_tag = soup.find('span', class_='d_book').find_all('a')
    book_genres = [tag.text for tag in book_genre_tag]

    return book_title, cover_image_url, comments, book_genres


def download_book_txt(book_id, filename, folder='Books/'):
    url = 'https://tululu.org/txt.php'
    payload = {'id': book_id}
    Path(f'./{folder}').mkdir(parents=True, exist_ok=True)

    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = Path(f'./{folder}/{sanitize_filename(filename)}.txt')

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_book_cover(url, filename, folder='Images/'):
    Path(f'./{folder}').mkdir(parents=True, exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    filepath = Path(f'./{folder}/{sanitize_filename(filename)}')

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def main():
    connection_waiting_seconds = 10

    parser = make_parser()
    if len(sys.argv) < 3:
        parser.print_help()
    args = parser.parse_args()

    for book_id in range(args.start_index, args.end_index + 1):
        is_connected = True
        tries_to_connect = 5

        while tries_to_connect > 0:
            try:
                response = get_book_page(book_id)
                book_title, cover_image_url, book_comments, book_genres = parse_book_page(response)
                txt_name = f'{book_id}. {book_title}'

                print(download_book_txt(book_id, txt_name))
                print(download_book_cover(cover_image_url, str(book_id)))
                print(book_genres) if book_genres else print('Для этой книги нет жанра')
                print(book_comments) if book_comments else print('У этой книги нет комментариев')
                break
            except requests.ConnectionError:
                if is_connected:
                    is_connected = False
                    print(f'Нет соединения')
                else:
                    print('Соединение не установлено')
                    print(f'Retrying connection via {connection_waiting_seconds} seconds.')
                    sleep(connection_waiting_seconds)
            except requests.HTTPError:
                print(f"Невозможно создать {txt_name}")
                break
            except Exception as error:
                print(f'Unexpected error: {error}')
                print(f'Ошибка загрузки "{txt_name}"')
            tries_to_connect -= 1


if __name__ == '__main__':
    main()
