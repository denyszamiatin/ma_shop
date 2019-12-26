create table users (
id serial primary key,
first_name varchar(50) not null,
second_name varchar (50),
email varchar (100) not null unique,
password varchar (255) not null
);