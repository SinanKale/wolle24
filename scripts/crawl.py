# Start the crawler. Remember to check settings.py do enable/disable the output of data to a file/db

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def get_regex(filters: list):
    """
    Get regex matching for existence of every word (case insensitive) in any place.
    :param filters: List of strings which will be split at ' ' each.
    :return: Generator containing regular expressions for each filter.
    """
    for filter_item in filters:
        words = filter_item.split(" ")
        word_filters = ""
        for word in words:
            word_filters += "(?=.*\\b{}\\b)".format(word)
        filter_regex = '(?i)^{}.+'.format(word_filters)
        yield filter_regex


if __name__ == "__main__":
    link_text_filter = ["dmc natura xl", "drops safran", "drops baby merino mix", "hahn alpacca speciale",
                        "stylecraft special double knit"]
    link_text_filter_regex = list(get_regex(link_text_filter))
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl('wollplatz', link_text_filter=link_text_filter_regex)
    process.start()
