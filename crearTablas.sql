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

CREATE SEQUENCE idAuthor INCREMENT 1
MINVALUE 173
START 173;

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
	num_books_per_loan INT4 CHECK(num_books_per_loan >= 0 AND num_books_per_loan <=7) DEFAULT 7,
	current_books INT4 DEFAULT 0,
    book_debt FLOAT8 CHECK(book_debt >= 0.0) DEFAULT 0.00,
	start_blocked_time timestamptz
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

CREATE TABLE Books_per_loan(
	id INT4 PRIMARY KEY,
	monto_libro_per_loan INT4 CHECK(monto_libro_per_loan >= 0 AND monto_libro_per_loan <=7) DEFAULT 7
);

CREATE TABLE Last_notification(
    id INT4 PRIMARY KEY,
    last_sent date
);

CREATE TABLE Politica_prestamo(
	id_ int,
	prestamos text,
	multas text,
	sanciones text
);

CREATE INDEX WrittenBy_index ON WrittenBy(book_id, author_id);

CREATE INDEX user_index ON CEIC_User(username, password_);

\COPY Author FROM './CSV/AutoresIndexados.csv' DELIMITER ',';

\COPY Book(title, authors, quantity, book_id) FROM './CSV/Codes.csv' DELIMITER ',' CSV HEADER;

\COPY WrittenBy FROM './CSV/writtenBy.csv' DELIMITER ',';

\COPY Book_copy(copy_id, book_id) FROM './CSV/CopyCodes.csv' DELIMITER ',';

INSERT INTO CEIC_User(username, password_, first_name, last_name, email, permission_mask, last_login, creation_date)
VALUES('Admin', crypt('prueba1', gen_salt('bf', 8)), 'Alan', 'Turing', 'ImitationGame@gmail.com', 1, now(), now());

INSERT INTO CEIC_User(username, password_, first_name, last_name, email, permission_mask, last_login, creation_date)
VALUES('User', crypt('prueba1', gen_salt('bf', 8)), 'Alan', 'Turing', 'ImitationGame@gmail.com', 0, now(), now());

INSERT INTO Estudiante(carnet, first_name, last_name, CI, phone, email)
VALUES('15-11095', 'Diego', 'Peña', 26122418, 04242486353, 'djpg98@gmail.com');

INSERT INTO Deuda(id, monto_deuda)
VALUES(0, 0.00);

INSERT INTO Last_notification(id, last_sent)
VALUES(0, current_date - interval '1 day');

INSERT INTO Books_per_loan(id, monto_libro_per_loan)
VALUES(0, 7);

INSERT INTO Politica_prestamo(id_, prestamos, multas, sanciones) VALUES (1, 'La duración de los préstamos variará por cada libro, y será definida por los miembros del CEIC. La cantidad máxima de libros por préstamo también será definida por los miembros del CEIC, y podrá ser modificada en cualquier momento. Un estudiante sólo podrá realizar un préstamo a la vez: para poder solicitar un nuevo libro, deberá finalizar primero cualquier préstamo que tenga en curso, si lo tiene.',
'El valor de las multas será modificado continuamente, y este podrá ser actualizado por los miembros del CEIC en cualquier momento al iniciar sesión en el sistema. El monto a pagar por una multa, para todo aquel estudiante endeudado, será incrementado cada día que pase sin que se devuelva algún o algunos de los libros bajo la fecha estipulada inicialmente para el préstamo correspondiente.',																	
'Las sanciones serán aplicadas a aquellos estudiantes que incumplan los plazos establecidos para la devolución de los libros prestados. El máximo tiempo que podrá durar una sanción será de 1 año (365 días). La aplicación de las sanciones a determinados estudiantes podrá ser decidido por los miembros del CEIC, y se podrá limitar el número de libros que podrán ser prestados a ese estudiante.');