create table novel_current_chapter
(
    openid varchar(32) not null,
    novel_name varchar(128) not null,
    novel_url varchar(256) not null,
   	novel_author varchar(128) not null,
    chapter_id varchar(128) not null,
    chapter_title varchar(128) not null, 
    chapter_url varchar(256) not null,
    novel_image varchar(256),
    novel_brief varchar(1024),
    novel_type varchar(128),
    novel_latest varchar(128)
);

create index novel_current_chapter on novel_current_chapter(openid, novel_url, chapter_id)