create table order_archive (
 id serial primary key,
 id_user integer references users(id),
 id_order integer references order(id),
 id_product integer references products(id),
 price decimal ,
 date_archive date
 );