Concession Scrapers for OpenOil.net
===================================

Scrapers for oil concessions coming from various sources, list with source urls and further description
can be found at:

* [Google Docs Spreadsheet](https://docs.google.com/spreadsheets/d/1nCo1nf3EU65Yw6_Td1P8jTMZCTArbB2vecUcekoR4mE/edit#gid=0)

Install Scrapy
--------------
[Python/Scrapy](http://scrapy.org/) is used for scrapers.

Install Scrapy following the [installation instructions](http://doc.scrapy.org/en/latest/intro/install.html)
from the website (version used for scraping was ``0.24``, possible to install concrete version with 
``pip install Scrapy==0.24``).

Install Sources from GitHub
---------------------------
[Git](http://git-scm.com/downloads) has to be installed on system.

Sources can then be cloned from Git repository from shell (or via GUI) with
``git clone https://github.com/holgerd77/openoil-concession-scrapers.git``. 

Usage
-----

A scraper can be run on the command line from within the ``scrapy_ooc`` directory with ``scrapy`` command
line tool.

The following command will scrape ``TN_ETAP_C`` scraper with screen output:

* ``scrapy crawl TN_ETAP_C``

The following command will save scraper output to CSV format:

* ``scrapy crawl -o TN_ETAP_C_Complete_2014-11-21.csv -t csv TN_ETAP_C``
