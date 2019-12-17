create table Comments (
	comment_id serial primary key,
    product_id integer references product(id),
    user_id integer references user(id),
    date TIMESTAMPTZ not null default NOW(),
    body TEXT
);