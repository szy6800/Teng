# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LoupanItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()
    id = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    domain = scrapy.Field()
    ProjName = scrapy.Field()
    PROPERTYADDITION = scrapy.Field()
    operastion = scrapy.Field()
    house_feature = scrapy.Field()
    buildCategory = scrapy.Field()
    FixStatus = scrapy.Field()
    right_desc = scrapy.Field()
    Round_oracle = scrapy.Field()
    developerAll = scrapy.Field()
    Address = scrapy.Field()
    salestatus = scrapy.Field()
    openhistory = scrapy.Field()
    livehistory = scrapy.Field()
    SaleAddress = scrapy.Field()
    telephone = scrapy.Field()
    GroundArea = scrapy.Field()
    PurposeArea = scrapy.Field()
    Dimension = scrapy.Field()
    VirescenceRate = scrapy.Field()
    ParkDesc = scrapy.Field()
    dongnum = scrapy.Field()
    TotalDoor = scrapy.Field()
    manager = scrapy.Field()
    property_fee = scrapy.Field()
    BuildingDes = scrapy.Field()
    ZONGFEN = scrapy.Field()
    price = scrapy.Field()
    pricetype = scrapy.Field()
    priceDateDesc = scrapy.Field()
    traffic = scrapy.Field()
    Layout = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    ProjDesc = scrapy.Field()
    # pass

'''
CREATE TABLE `ershou` (
  `uid` varchar(255) DEFAULT NULL,
  `id` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `ProjName` varchar(255) DEFAULT NULL,
  `PROPERTYADDITION` varchar(255) DEFAULT NULL,
  `operastion` varchar(255) DEFAULT NULL,
  `house_feature` varchar(255) DEFAULT NULL,
  `buildCategory` varchar(255) DEFAULT NULL,
  `FixStatus` varchar(255) DEFAULT NULL,
  `right_desc` varchar(255) DEFAULT NULL,
  `Round_oracle` varchar(255) DEFAULT NULL,
  `developerAll` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `salestatus` varchar(255) DEFAULT NULL,
  `openhistory` varchar(255) DEFAULT NULL,
  `livehistory` varchar(255) DEFAULT NULL,
  `SaleAddress` varchar(255) DEFAULT NULL,
  `telephone` varchar(255) DEFAULT NULL,
  `GroundArea` varchar(255) DEFAULT NULL,
  `PurposeArea` varchar(255) DEFAULT NULL,
  `Dimension` varchar(255) DEFAULT NULL,
  `VirescenceRate` varchar(255) DEFAULT NULL,
  `ParkDesc` varchar(255) DEFAULT NULL,
  `dongnum` varchar(255) DEFAULT NULL,
  `TotalDoor` varchar(255) DEFAULT NULL,
  `manager` varchar(255) DEFAULT NULL,
  `property_fee` varchar(255) DEFAULT NULL,
  `BuildingDes` varchar(255) DEFAULT NULL,
  `ZONGFEN` varchar(255) DEFAULT NULL,
  `price` varchar(255) DEFAULT NULL,
  `pricetype` varchar(255) DEFAULT NULL,
  `priceDateDesc` varchar(255) DEFAULT NULL,
  `traffic`  text,
  `Layout` varchar(255) DEFAULT NULL,
  `lng` varchar(255) DEFAULT NULL,
  `lat` varchar(255) DEFAULT NULL,
  `ProjDesc`  text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''