create table mark (
    id serial primary key,
    id_user integer references users(id),
    id_product integer references products(id),
    mark_date date default current_date,
    rating integer
);
