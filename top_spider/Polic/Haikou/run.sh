#! /bin/bash
export PATH=$PATH:/usr/local/bin
cd /root/spiders/Polic/Haikou
scrapy crawl Technology;scrapy crawl Education;scrapy crawl Market;scrapy crawl Tax;scrapy crawl Human;scrapy crawl Gov;