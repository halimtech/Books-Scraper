from bs4 import BeautifulSoup
from locators.book_page_locators import BookPage
from parsing.book import BookParser
import logging
import re

logger = logging.getLogger('scrapping_all_books')


class BookComplete:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all books in the page using `{BookPage.BOOK_LOCATOR}`')
        return [BookParser(e) for e in self.soup.select(BookPage.BOOK_LOCATOR)]

    @property
    def page_count(self):
        logger.debug('Finding all number of catalogue pages available...')
        content = self.soup.select_one(BookPage.PAGE).string
        logger.info(f'Found number of catalogue pages available: `{content}`')
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.info(f'Extracted number of pages as integer: `{pages}`.')
        return pages
