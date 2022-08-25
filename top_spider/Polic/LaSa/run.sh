#! /bin/bash
export PATH=$PATH:/usr/local/bin
cd /root/spiders/Polic/LaSa
scrapy crawl Technology;scrapy crawl Education;scrapy crawl Maket;scrapy crawl Tax_Notice;scrapy crawl Tax_Policy;scrapy crawl Human;scrapy crawl Gov;
