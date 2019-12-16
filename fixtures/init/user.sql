CREATE TABLE user(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(35) NOT NULL,
    second_name VARCHAR (50),
    email VARCHAR (50) NOT NULL unique,
    password VARCHAR (25) NOT NULL
)