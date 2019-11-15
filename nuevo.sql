CREATE TABLE Book(
	book_id INT4 PRIMARY KEY CHECK(book_id <= 9999 AND book_id >= 0),
	title VARCHAR(100),
	authors VARCHAR(100),
	isbn VARCHAR(100) DEFAULT 'NA',
	quantity INT4,
	quantity_lent INT4 DEFAULT 0, 
	loan_duration INT4 DEFAULT 7 --Recordar cambiar esto luego de hablar con el CEIC
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

\COPY Author FROM './CSV/AutoresIndexados.csv' DELIMITER ',';

\COPY Book(title, authors, quantity, book_id) FROM './CSV/Codes.csv' DELIMITER ',' CSV HEADER;

\COPY WrittenBy FROM './CSV/writtenBy.csv' DELIMITER ',';

\COPY Book_copy(copy_id, book_id) FROM './CSV/CopyCodes.csv' DELIMITER ',';

CREATE INDEX WrittenBy_index ON WrittenBy(book_id, author_id);

INSERT INTO Deuda(id, monto_deuda)
VALUES(0, 0.00);
