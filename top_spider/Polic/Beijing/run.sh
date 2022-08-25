#! /bin/bash
export PATH=$PATH:/usr/local/bin
cd /root/spiders/Polic/Beijing
scrapy crawl Commerce;scrapy crawl Economics;scrapy crawl Finance;scrapy crawl Technology;scrapy crawl Education;scrapy crawl Market;scrapy crawl Banking;scrapy crawl Tax;scrapy crawl Human;scrapy crawl Gov;
