# Tululu__parsing

Скрипт, который скачивает книги с ресурса Tululu.org, а также ее составляющие, такие как:
1. Название
2. Жанр
3. Обложка

Обложка книги скачивается в папку "Images", а текстовый файл в папку "Books".

## Установка 
1. Скачайте репозиторий
2. Python3+ должен быть уже установлен
3. Установите зависимости:
   
   `pip install -r requirements.txt`
   
## Использование
В терминале перейдите в директорию проекта и запустите скрипт командой:
   
 `python main.py 2 15`
   
Числа в данном случае - id книг со 2 по 15. Скрипт начнет скачивание текстовых файлов и изображений обложки в соответствующие директории.
Директории создавать не нужно, они будут созданы автоматически. 
