create table novel_bookshelf
(
    openid varchar(32) not null,
    novel_name varchar(128) not null,
    novel_url varchar(256) not null,
   	novel_author varchar(128) not null,
    novel_image varchar(256),
    novel_brief varchar(1024),
    novel_type varchar(128),
    novel_latest varchar(128)
);

create index index_novel_shelf on novel_bookshelf(openid, novel_url)