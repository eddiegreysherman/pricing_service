import uuid
import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.url = url
        self.name = name
        #self.name = self.get_item_name()
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())

        return self.price

    # def get_item_name(self):
    #     request = requests.get(self.url)
    #     content = request.content
    #     soup = BeautifulSoup(content, "html.parser")
    #     element = soup.find("span", {"itemprop": "name"})
    #     item_name = element.text.strip()
    #
    #     return item_name


    def save_to_mongo(self):
        # insert json representation
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "_id": self._id,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))