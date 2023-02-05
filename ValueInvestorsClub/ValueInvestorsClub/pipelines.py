# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# This pipeline will dump the associated data into a postgres sql database.

from itemadapter import ItemAdapter
from sqlalchemy import create_engine

class SqlPipeline:
    collection_name = 'scrapy_items'

    def __init__(self, postgres_uri, sql_db):
        self.postgres_uri = postgres_uri
        self.sql_db = sql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sql_uri=crawler.settings.get('POSTGRES_URI'),
            sql_db=crawler.settings.get('POSTGRESS_DB', 'ValueInvestorsClub')
        )

    def open_spider(self, spider):
        engine = create_engine('postgresql+psycopg2://user:password\@hostname/database_name')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
