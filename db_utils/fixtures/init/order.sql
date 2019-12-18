create table orders(
    id serial primary key,
    id_user integer references user(id),
    id_product integer references products(id),
    price decimal not null,
    order_date date default current_date
);