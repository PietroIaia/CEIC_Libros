CREATE TABLE Politica_prestamo(
	id_ int,
	prestamos text,
	multas text,
	sanciones text
);

INSERT INTO Politica_prestamo(id_, prestamos, multas, sanciones) VALUES (1, 'La duración de los préstamos variará por cada libro, y será definida por los miembros del CEIC. La cantidad máxima de libros por préstamo también será definida por los miembros del CEIC, y podrá ser modificada en cualquier momento. Un estudiante sólo podrá realizar un préstamo a la vez: para poder solicitar un nuevo libro, deberá finalizar primero cualquier préstamo que tenga en curso, si lo tiene.',
'El valor de las multas será modificado continuamente, y este podrá ser actualizado por los miembros del CEIC en cualquier momento al iniciar sesión en el sistema. El monto a pagar por una multa, para todo aquel estudiante endeudado, será incrementado cada día que pase sin que se devuelva algún o algunos de los libros bajo la fecha estipulada inicialmente para el préstamo correspondiente.',																	
'Las sanciones serán aplicadas a aquellos estudiantes que incumplan los plazos establecidos para la devolución de los libros prestados. El máximo tiempo que podrá durar una sanción será de 1 año (365 días). La aplicación de las sanciones a determinados estudiantes podrá ser decidido por los miembros del CEIC, y se podrá limitar el número de libros que podrán ser prestados a ese estudiante.');

