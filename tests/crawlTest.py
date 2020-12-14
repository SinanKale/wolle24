import unittest
from scrapy.http import HtmlResponse
from wolle24.spiders.wollplatz_spider import WollplatzSpider


def fake_response(response_file_path, response_url='https://wollplatz.de', file_encoding='utf-8'):
    with open(response_file_path, 'r', encoding=file_encoding) as f:
        content = f.read()
    response = HtmlResponse(url=response_url, body=content, encoding=file_encoding)
    return response


class WollplatzSpiderTest(unittest.TestCase):
    def test_parse_items_fake_full(self):
        spider = WollplatzSpider()
        result = spider.parse_items(fake_response('dmc-natura-xl.html'))
        item = next(result)
        self.assertEqual(item['product_name'], 'Natura XL')
        self.assertEqual(item['product_brand'], 'DMC')
        self.assertEqual(item['product_price'], '8,05')
        self.assertEqual(item['product_price_currency'], '€')
        self.assertEqual(item['product_delivery'], 'Lieferbar')
        self.assertEqual(item['product_needle_size'], '8 mm')
        self.assertEqual(item['product_material'], '100% Baumwolle')

    def test_parse_items_fake_partial(self):
        spider = WollplatzSpider()
        result = spider.parse_items(fake_response('catania-trend-garnpaket.html'))
        item = next(result)
        self.assertIsNot(item, 'product_needle_size')
        self.assertIsNot(item, 'product_material')
        self.assertEqual(item['product_name'], 'Catania Trend Garnpaket')
        self.assertEqual(item['product_brand'], 'Schachenmayr')
        self.assertEqual(item['product_price'], '24,75')
        self.assertEqual(item['product_price_currency'], '€')
        self.assertEqual(item['product_delivery'], 'Lieferbar')

    def test_parse_items_fake_none(self):
        spider = WollplatzSpider()
        result = spider.parse_items(fake_response('home.html'))
        item = next(result)
        self.assertIsNot(item, 'product_name')
        self.assertIsNot(item, 'product_brand')
        self.assertIsNot(item, 'product_price')
        self.assertIsNot(item, 'product_price_currency')
        self.assertIsNot(item, 'product_delivery')
        self.assertIsNot(item, 'product_needle_size')
        self.assertIsNot(item, 'product_material')


if __name__ == '__main__':
    unittest.main()
