-- CEIC Libros
-- Tabla de estudiantes
-- Desarrollado por Forward
-- Responsable del módulo: Diego Peña, 15-11095
-- Fecha de inicio: 14-10-19, no recuerdo la hora, pero debe haber sido tarde-noche
-- Última modifcación: 21-10-19, 22:02, Hora de Venezuela

-- Tablas básicas y algunos datos de prueba

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

CREATE TABLE Estudiante(
	carnet CHAR(8) PRIMARY KEY,
	first_name VARCHAR(32) NOT NULL,
	last_name VARCHAR(32) NOT NULL,
	CI INT4 UNIQUE NOT NULL,
	phone VARCHAR(12),
	email VARCHAR(36),
	days_blocked INT4 CHECK(days_blocked >= 0) DEFAULT 0,
	current_books INT4 DEFAULT 0,
    book_debt FLOAT8 CHECK(book_debt >= 0.0) DEFAULT 0.00
);

CREATE INDEX user_index ON CEIC_User(username, password_);

INSERT INTO CEIC_User(username, password_, first_name, last_name, email, permission_mask, last_login, creation_date)
VALUES('Admin', crypt('prueba1', gen_salt('bf', 8)), 'Alan', 'Turing', 'ImitationGame@gmail.com', 1, now(), now())

INSERT INTO Estudiante(carnet, first_name, last_name, CI, phone, email)
VALUES('15-11095', 'Diego', 'Peña', 26122418, 04242486353, 'djpg98@gmail.com');