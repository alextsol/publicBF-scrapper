# pipelines.py

import pymongo
from itemadapter import ItemAdapter
import datetime

class MongoPipeline:
    collection_name = 'public_items'  # Change to your preferred collection name

    def open_spider(self, spider):
        # Connecting to the MongoDB database
        self.client = pymongo.MongoClient('localhost', 27017) # adjust it to your database
        self.db = self.client["scrapy_db"]  # Database name

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Add timestamp
        item['date'] = datetime.datetime.now()

        # Insert into MongoDB
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
