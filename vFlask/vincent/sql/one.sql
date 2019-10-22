drop table spider_one;
create table SPIDER_ONE
(
  spider_index varchar(128) not null,
  spider_date varchar(20) not null,
  spider_result LONGTEXT,
  spider_url varchar(512)
);

create unique index index_spider_one on spider_one(spider_index, spider_date);