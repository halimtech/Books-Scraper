import re
import logging
from locators.books_locators import BookLocators

logger = logging.getLogger('scrapping.book_parser')


class BookParser:
    """
    Finding the price name and rating of a book in the weebsite
    """

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        logger.debug(f'New book parser created from `{parent}`')
        self.parent = parent

    def __repr__(self):
        return f'<Book {self.name}, costs {self.price}, {self.rating} stars>'

    @property
    def name(self):
        logger.debug('Finding book name...')
        locator = BookLocators.NAME
        item_name = self.parent.select_one(locator).attrs['title']
        logger.info(f'Found book name, `{item_name}`.')
        return item_name

    @property
    def link(self):
        logger.debug('Finding book page link...')
        locator = BookLocators.LINK
        item_url = self.parent.select_one(locator).attrs['href']
        logger.info(f'Found book page link, `{item_url}`.')
        return item_url

    @property
    def price(self):
        logger.debug('Finding book price...')
        locator = BookLocators.PRICE
        price_str = self.parent.select_one(locator).string
        logger.debug(f'Item price element found, `{price_str}`')
        expr = '£([0-9]+\.[0-9]+)'
        matches = re.search(expr, price_str)
        price = float(matches.group(1))
        logger.info(f'Found book price, `{price}`.')
        return price

    @property
    def rating(self):
        logger.debug('Finding the star rating....')
        locator = BookLocators.RATING
        star_rating_tag = self.parent.select_one(locator)
        classes = star_rating_tag.attrs['class']  # ['star-rating' , 'Three']
        rating = [p for p in classes if p != 'star-rating']
        logger.debug(f'Found the rating class{rating}')
        rating_int = BookParser.RATINGS.get(rating[0])
        return rating_int
