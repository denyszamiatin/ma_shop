create table Comments (
	id serial primary key,
    id_product integer references product(id),
    id_user integer references users(id),
    comment_date TIMESTAMPTZ not null default NOW(),
    body TEXT
);