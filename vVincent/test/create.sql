create table vincent_user
(
	user_name	varchar(30) not null,
	user_pswd	varchar(32) not null
);

create unique index index_v_user on vincent_user(user_name)
