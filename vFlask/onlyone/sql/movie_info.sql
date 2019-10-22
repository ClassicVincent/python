drop table movie_info;
create table MOVIE_INFO
(
	movie_name VARCHAR (128) NOT NULL,
	movie_name_tag VARCHAR (128) NOT NULL,
	movie_source VARCHAR (16) NOT NULL ,
	movie_download_url VARCHAR (1024) NOT NULL ,
	movie_page_url VARCHAR (256) NOT NULL,
	movie_date varchar(16) not null,
	is_main_page varchar(2)
);

create UNIQUE index index_movie_info on MOVIE_INFO(movie_tag_name, movie_source, movie_page_url);
create index index_movie_info1 on movie_info(movie_source, movie_page_url);
