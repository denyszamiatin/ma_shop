create table news (
    id_news serial primary key,
    title varchar(255),
    post varchar(max),
    id_user integer references user(id),
    news_date date
);
