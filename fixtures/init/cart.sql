create table cart (
 id serial primary key,
 id_user integer references user(id),
 id_product integer references product_category(id),
 addition_date date 
 );
