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

\COPY Author FROM './CSV/AutoresIndexados.csv' DELIMITER ',';

\COPY Book(title, authors, quantity, book_id) FROM './CSV/Codes.csv' DELIMITER ',' CSV HEADER;

\COPY WrittenBy FROM './CSV/writtenBy.csv' DELIMITER ',';

CREATE INDEX WrittenBy_index ON WrittenBy(book_id, author_id);
