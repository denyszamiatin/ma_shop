create table news (
    id serial primary key,
    title varchar(255) not null,
    post text not null,
    id_user integer references user(id),
    news_date date not null
);
