create table product_categories (
id serial primary key,
name varchar(255) unique
);

grant all privileges on table product_categories to task_admin;
grant all on sequence product_categories_id_seq to task_admin;
