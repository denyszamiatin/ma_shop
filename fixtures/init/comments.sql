CREATE TABLE Comments (
	comment_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES product(id),
    user_id INTEGER REFERENCES user(id),
    date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    body TEXT
);