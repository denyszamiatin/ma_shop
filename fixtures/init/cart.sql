create table cart (
 id serial primary key,
 id_user integer not null references user(id),
 id_product integer not null references product_category(id),
 addition_date date default current_date
 );
