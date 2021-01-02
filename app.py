import requests
import logging
import time

from pages.books_page import BookComplete

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')
logger = logging.getLogger('scraping')

logger.info('Requesting http://books.toscrape.com')
page_content = requests.get('http://books.toscrape.com').content
logger.debug('Creating AllBooksPage from page content.')
page = BookComplete(page_content)

_books = []
start = time.time()

logger.info(f'Going through {page.page_count} pages of books...')
loop = asyncio.get_event_loop()

async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(50):
        async with session.get(url) as response:
            print(f'page took {time.time() - page_start}')
            return await response.text()


async def get_multiple_pages(*urls2):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls2:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks


urls = [f'http://books.toscrape.com/catalogue/page-{i+ 1}.html' for i in range(page.page_count)]

pages = loop.run_until_complete(get_multiple_pages(*urls))
for page_content in pages:
    logger.debug('Creating AllBooksPage from page content.')
    page = BookComplete(page_content)
    _books.extend(page.books)

print(f'Total took {time.time() - start}')

bookse = _books
