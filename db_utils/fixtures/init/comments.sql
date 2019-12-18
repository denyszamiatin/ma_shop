create table Comments (
	id serial primary key,
    product_id integer references product(id),
    user_id integer references user(id),
    comment_date TIMESTAMPTZ not null default NOW(),
    body TEXT
);