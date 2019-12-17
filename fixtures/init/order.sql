create table orders(
    id serial primary key,
    id_user integer references user(user_id),
    id_product integer references products(Id),
    price decimal not null,
    order_date date not null
);