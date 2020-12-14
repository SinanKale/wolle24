from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import Wolle24Item
from scrapy.loader import ItemLoader


class WollplatzSpider(CrawlSpider):
    name = 'wollplatz'

    def __init__(self, link_text_filter=None, allowed_domains=None,
                 start_urls=None, *args, **kwargs):
        """
        :param link_text_filter: List of regular expressions. A request to the product link will only be made and parsed
               if one of the expressions matches. The crawler will parse every product page if None.
        :param allowed_domains: Domains that are allowed to crawl.
        :param start_urls: Urls to start crawling. Should be the list of products.
        """
        if allowed_domains is None:
            allowed_domains = ['wollplatz.de']
        if start_urls is None:
            start_urls = ['https://wollplatz.de/wolle']
        WollplatzSpider.allowed_domains = allowed_domains
        WollplatzSpider.start_urls = start_urls
        WollplatzSpider.rules = (
            Rule(LinkExtractor(restrict_css='link[rel=next]', tags=['link']), follow=True),
            Rule(LinkExtractor(restrict_css='.gtm-product-impression a',
                               restrict_text=link_text_filter),
                 callback='parse_items', follow=False),
        )
        super(WollplatzSpider, self).__init__(*args, **kwargs)

    def parse_items(self, response):
        # There is no product name on the page, thus the title and brand is used to assume it.
        product_name = response.css('.variants-title-txt').css('::text').get() or response.css('#pageheadertitle').css(
            '::text').get() or None
        product_specs = response.css('#pdetailTableSpecs td').css('::text').getall()
        product_specs = dict(zip(product_specs[::2], product_specs[1::2]))
        product_brand = product_specs.get('Marke')
        product_material = product_specs.get('Zusammenstellung')
        product_needle_size = product_specs.get('Nadelstärke')
        if product_name and (product_brand in product_name):
            product_name = product_name.replace(product_brand, '')

        loader = ItemLoader(Wolle24Item(), response=response)
        loader.add_css('product_price', '.product-price .product-price-amount::text')
        loader.add_css('product_price_currency', '.product-price .product-price-currency::text')
        loader.add_css('product_delivery', '.pbuy-voorraad td span::text')
        loader.add_value('product_needle_size', product_needle_size)
        loader.add_value('product_material', product_material)
        loader.add_value('product_brand', product_brand)
        loader.add_value('product_name', product_name)
        loader.add_value('url', response.url)
        yield loader.load_item()
