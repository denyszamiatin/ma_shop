create table order_archive (
 archive_id serial primary key,
 user_id integer references user(user_id),
 order_id integer references order(id_order),
 product_id integer references products(Id),
 price INTEGER,
 date date
 );