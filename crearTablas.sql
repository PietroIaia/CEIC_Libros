-- CEIC Libros
-- Tabla de estudiantes
-- Desarrollado por Forward
-- Responsable del módulo: Diego Peña, 15-11095
-- Fecha de inicio: 14-10-19, no recuerdo la hora, pero debe haber sido tarde-noche
-- Última modifcación: 21-10-19, 22:02, Hora de Venezuela

-- Constraint en book_copy. Agregado Author y writtenBy
CREATE DATABASE pruebaceic;

\c pruebaceic

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

CREATE TABLE Book(
	book_id INT4 PRIMARY KEY CHECK(book_id <= 9999 AND book_id >= 0),
	title VARCHAR(100),
	authors VARCHAR(100),
	isbn VARCHAR(100) DEFAULT 'NA',
	quantity INT4,
	quantity_lent INT4 DEFAULT 0, 
	loan_duration INT4 DEFAULT 7 --Recordar cambiar esto luego de hablar con el CEIC
);

CREATE TABLE Book_copy(
	copy_id INT4 CHECK(copy_id <= 99 AND copy_id >= 0), 
	book_id INT4 REFERENCES Book(book_id),
	edition INT4 DEFAULT NULL,
	ed_year INT4 DEFAULT NULL,
	ed_language VARCHAR(32) DEFAULT NULL,
	PRIMARY KEY(book_id, copy_id)
);

CREATE TABLE Loan(
	carnet CHAR(8) REFERENCES Estudiante(carnet),
	book_id INT4,
	copy_id INT4,
	lender VARCHAR(32) REFERENCES CEIC_User(username),
	receiver VARCHAR(32) REFERENCES CEIC_User(username),
	start_time timestamptz,
	estimated_return_time timestamptz,
	return_time timestamptz,
	FOREIGN KEY(book_id, copy_id) REFERENCES Book_Copy(book_id, copy_id),
	PRIMARY KEY(carnet, book_id, copy_id, start_time)
);

CREATE TABLE Author(
    first_name VARCHAR(32),
    last_name VARCHAR(64),
    author_id INT4 PRIMARY KEY
);

CREATE TABLE WrittenBy(
    book_id INT4 REFERENCES Book(book_id),
    author_id INT4 REFERENCES Author(author_id),
    PRIMARY KEY(book_id, author_id)
);

CREATE TABLE Transferencias(
	username VARCHAR(32) REFERENCES CEIC_User(username),
	cliente CHAR(8) REFERENCES Estudiante(carnet),
	monto FLOAT8 CHECK(monto >= 0.0) DEFAULT 0.00,
	banco TEXT NOT NULL,
	codigo VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Deuda(
	id INT4 PRIMARY KEY,
	monto_deuda FLOAT8 CHECK(monto_deuda >= 0.0) DEFAULT 0.00
);

CREATE INDEX WrittenBy_index ON WrittenBy(book_id, author_id);

CREATE INDEX user_index ON CEIC_User(username, password_);

\COPY Author FROM './CSV/AutoresIndexados.csv' DELIMITER ',';

\COPY Book(title, authors, quantity, book_id) FROM './CSV/Codes.csv' DELIMITER ',' CSV HEADER;

\COPY WrittenBy FROM './CSV/writtenBy.csv' DELIMITER ',';

INSERT INTO CEIC_User(username, password_, first_name, last_name, email, permission_mask, last_login, creation_date)
VALUES('Admin', crypt('prueba1', gen_salt('bf', 8)), 'Alan', 'Turing', 'ImitationGame@gmail.com', 1, now(), now());

INSERT INTO CEIC_User(username, password_, first_name, last_name, email, permission_mask, last_login, creation_date)
VALUES('User', crypt('prueba1', gen_salt('bf', 8)), 'Alan', 'Turing', 'ImitationGame@gmail.com', 0, now(), now());

INSERT INTO Estudiante(carnet, first_name, last_name, CI, phone, email)
VALUES('15-11095', 'Diego', 'Peña', 26122418, 04242486353, 'djpg98@gmail.com');

INSERT INTO Deuda(id, monto_deuda)
VALUES(0, 0.00);