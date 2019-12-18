create table mark (
    id serial primary key,
    id_user integer references user(id),
    id_product integer references product(id),
    mark_date date,
    rating integer
);
