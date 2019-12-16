create table Order_(
    id_order serial primary key,
    id_user integer references user(id),
    id_product integer references products(Id),
    price integer
    order_date date
);