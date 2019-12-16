create table Archive (
 id serial primary key,
 id_user integer references user(id_user),
 id_order integer references order(id_order),
 id_product integer references product(Id),
 price INTEGER,
 date date
 );