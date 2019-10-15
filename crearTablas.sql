CREATE EXTENSION pgcrypto;

CREATE TABLE CEIC_User(
    username VARCHAR(32) PRIMARY KEY,
    password_ TEXT NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    permission_mask INT4 NOT NULL,
    last_login timestamptz,
    creation_date timestamptz
);

CREATE INDEX user_index ON CEIC_User(username, password_);

INSERT INTO CEIC_User(username, password_, first_name, last_name, email, permission_mask, last_login, creation_date)
VALUES('Admin', crypt('prueba1', gen_salt('bf', 8)), 'Alan', 'Turing', 'ImitationGame@gmail.com', 1, now(), now())