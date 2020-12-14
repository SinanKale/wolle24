# Wolle24

Web Crawler using scrapy to get product information from _wollplatz.de_. 
Starting point for the implemented spider is _https://www.wollplatz.de/wolle_ by default.

## Usage

Start crawling by calling the _crawl.py_ script in the _scripts_ directory.
The crawler will persists data to a database or file depending on the settings in the _settings.py_ file.

In order to filter the crawled results by their title, you can pass a list of regular expressions to the implemented spider _WollplatzSpider_
If one of the passed expressions matches, the corresponding product page will be crawled. If no expressions are passed, every found product page will be crawled.

The filter in _crawl.py_ is set to only match for the following product titles:
* DMC Natura XL
* Drops Safran
* Drops Baby Merino Mix
* Hahn Alapacca Speciale
* Stylecraft Special double knit 

### Save crawled items:

* **Database**:
A simple database Pipeline was implemented in order to save the crawled items to a mysql database.
Uncomment the _ITEM_PIPELINES_ dictionary in the _settings.py_ file in order to save the crawled items in a mysql database.
Also edit the _DB_SETTINGS_ dictionary in the _settings.py_ file to match your environment.
The database used can be created using the _wolle24.sql_ in the _docs_ directory

* **File**:
Uncomment the _FEED_FORMAT_ and _FEED_URI_ variables in the _settings.py_ file in order to save the crawled items as _.csv_ file.