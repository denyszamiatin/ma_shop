CREATE TABLE Comments (
	comment_id SERIAL PRIMARY KEY,
    product_id integer references product(id),
    user_id integer references user(id),
    date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    body TEXT
);

--db.execute("""create table comments (
--        comment_id integer primary key,
--        product_id integer,
--        date timestamp default CURRENT_TIMESTAMP,
--        body varchar(200),
--        user_id integer,
--        foreign key (product_id) references products(product_id),
--        foreign key (user_id) references users(user_id)
--)""")