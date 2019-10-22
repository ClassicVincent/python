use vincent;
drop table session;
create table session
(
	name	VARCHAR(128) NOT NULL,
	value	LONGTEXT
);

create index index_session on session(name);
