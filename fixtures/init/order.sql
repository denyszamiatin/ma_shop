create table Order (
    id_order serial primary key,
    id_user integer references user(id),
    id_product integer references products(ProductID),
    price integer references products(Price),
    order_date date
);