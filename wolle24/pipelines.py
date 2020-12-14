# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import NotConfigured
import mysql.connector


class Wolle24Pipeline:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        database_settings = crawler.settings.get("DB_SETTINGS")
        if not database_settings:
            raise NotConfigured
        return cls(database_settings['host'], database_settings['database'], database_settings['user'],
                   database_settings['password'],
                   )

    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            auth_plugin='mysql_native_password',
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        insert_sql = "INSERT INTO crawled_items (crawler, source, brand, name, price, currency, delivery, needle_size, material) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            spider.name, item.get('url'), item.get('product_brand'), item.get('product_name'),
            float(item.get('product_price').replace(',', '.')),
            item.get('product_price_currency'), item.get('product_delivery'),
            item.get('product_needle_size'), item.get('product_material'))
        try:
            self.cursor.execute(insert_sql)
            self.connection.commit()
        except:
            self.connection.rollback()
        return item
