use vincent;
drop table onlyone_user;
create table onlyone_user
(
	user_name	VARCHAR(128) NOT NULL,
	user_pswd	VARCHAR(32) NOT NULL
);

create index index_session on onlyone_user(user_name);
