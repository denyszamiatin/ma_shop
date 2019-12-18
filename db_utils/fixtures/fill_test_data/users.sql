create EXTENSION pgcrypto;
insert into users (first_name, second_name, email, password) VALUES ('Ivan','Ivanov','ivanov@gmail.com',crypt("gfhjkm123",gen_salt('bf')));
insert into users (first_name, second_name, email, password) VALUES ('Roman','Petrenko','petrenko@gmail.com',crypt("admin123",gen_salt('bf')));
