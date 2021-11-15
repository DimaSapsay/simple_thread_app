import datetime
import pickle
import time
import threading

import requests

from loguru import logger
from urlextract import URLExtract


logger.add(
    "logfile_.log",
    rotation=datetime.timedelta(minutes=5),
    retention=datetime.timedelta(minutes=20)
)

original_urls_data = {}
unshorten_urls_data = {}


def get_urls():
    with open('messages_to_parse.dat', 'rb') as f:
        infile = f.read()
        message_lst = pickle.loads(infile)
        message = ' '.join(message_lst)

    logger.info('successful file opening')

    extractor = URLExtract()
    urls = extractor.find_urls(message)

    return urls


def head_response(url):
    try:
        response = requests.head(url, timeout=3)
        original_urls_data[url] = response.status_code

    except Exception as e:
        logger.error(e)


def get_response(url):
    try:
        response = requests.get(url, timeout=3)
        unshorten_urls_data[url] = response.url

    except Exception as e:
        logger.error(e)


def threading_func(urls, func):
    threads = []
    for url in urls:
        t = threading.Thread(target=func, args=[url])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


def main():
    start = time.time()

    logger.info('starting the program')

    urls = get_urls()

    threading_func(urls, head_response)

    unshorten_urls = []
    for url, status in original_urls_data.items():
        if 300 <= status < 400:
            unshorten_urls.append(url)

    if unshorten_urls:
        threading_func(unshorten_urls, get_response)

    logger.info('finishing the program')

    end = time.time()
    logger.info(f"The time of execution of above program is :{end-start}")


if __name__ == "__main__":
    main()
