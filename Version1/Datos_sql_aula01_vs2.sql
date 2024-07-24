-- Usar la base de datos aula01
USE aula01;

-- Insertar registros en la tabla direccion
INSERT INTO direccion (id, calle, numero, codigoP) VALUES 
(1, 'Calle Falsa', 123, 1001),
(2, 'Av. Siempreviva', 742, 1002),
(3, 'Calle Corrientes', 800, 1003),
(4, 'Calle Lavalle', 350, 1004),
(5, 'Calle Florida', 456, 1005),
(6, 'Calle Maipú', 789, 1006),
(7, 'Calle Córdoba', 101, 1007),
(8, 'Calle San Martín', 202, 1008),
(9, 'Calle Rivadavia', 303, 1009),
(10, 'Calle Belgrano', 404, 1010);

-- Insertar registros en la tabla mensajes
INSERT INTO mensajes (id_mensaje, mensaje) VALUES 
(1, 'Falta Dato'),
(2, 'Falta Curso'),
(3, 'Falta Instructor'),
(4, 'Falta Alumno'),
(5, 'Error de Ingreso'),
(6, 'Error de Sistema');

-- Insertar registros en la tabla educacion
INSERT INTO educacion (id_educacion, educacionMax, institucion, titulo) VALUES 
(1, 'Secundaria', 'Instituto A', 'Bachiller'),
(2, 'Terciaria', 'Instituto B', 'Técnico'),
(3, 'Universitaria', 'Universidad C', 'Licenciado'),
(4, 'Maestría', 'Universidad D', 'Magíster'),
(5, 'Doctorado', 'Universidad E', 'Doctor'),
(6, 'Secundaria', 'Instituto F', 'Bachiller'),
(7, 'Terciaria', 'Instituto G', 'Técnico'),
(8, 'Universitaria', 'Universidad H', 'Licenciado'),
(9, 'Maestría', 'Universidad I', 'Magíster'),
(10, 'Doctorado', 'Universidad J', 'Doctor');

-- Insertar registros en la tabla educacionInst
INSERT INTO educacionInst (id_educacion, educacionMax, institucion, titulo) VALUES 
(1, 'Secundaria', 'Instituto K', 'Bachiller'),
(2, 'Terciaria', 'Instituto L', 'Técnico'),
(3, 'Universitaria', 'Universidad M', 'Licenciado'),
(4, 'Maestría', 'Universidad N', 'Magíster'),
(5, 'Doctorado', 'Universidad O', 'Doctor'),
(6, 'Secundaria', 'Instituto P', 'Bachiller'),
(7, 'Terciaria', 'Instituto Q', 'Técnico'),
(8, 'Universitaria', 'Universidad R', 'Licenciado'),
(9, 'Maestría', 'Universidad S', 'Magíster'),
(10, 'Doctorado', 'Universidad T', 'Doctor');

-- Insertar registros en la tabla cursos
INSERT INTO cursos (codigo, nombre, descripcion) VALUES 
(1, 'Matemáticas', 'Curso de Matemáticas Básicas'),
(2, 'Física', 'Curso de Física General'),
(3, 'Química', 'Curso de Química Orgánica'),
(4, 'Historia', 'Curso de Historia Universal'),
(5, 'Geografía', 'Curso de Geografía Física'),
(6, 'Literatura', 'Curso de Literatura Clásica'),
(7, 'Biología', 'Curso de Biología Celular'),
(8, 'Filosofía', 'Curso de Filosofía Moderna'),
(9, 'Arte', 'Curso de Historia del Arte'),
(10, 'Informática', 'Curso de Programación Básica');

-- Insertar registros en la tabla alumnos
INSERT INTO alumnos (dni, nombre, apellido, direccion, educacion) VALUES 
(12345678, 'Juan', 'Pérez', 1, 1),
(23456789, 'Ana', 'Gómez', 2, 2),
(34567890, 'Luis', 'Martínez', 3, 3),
(45678901, 'María', 'Rodríguez', 4, 4),
(56789012, 'Carlos', 'López', 5, 5),
(67890123, 'Sofía', 'González', 6, 6),
(78901234, 'Pedro', 'Sánchez', 7, 7),
(89012345, 'Lucía', 'Ramírez', 8, 8),
(90123456, 'Jorge', 'Torres', 9, 9),
(12340987, 'Elena', 'Hernández', 10, 10);

-- Insertar registros en la tabla instructores
INSERT INTO instructores (dni, nombre, apellido, direccion, educacion) VALUES 
(22334455, 'Miguel', 'Suárez', 1, 1),
(33445566, 'Clara', 'Morales', 2, 2),
(44556677, 'Héctor', 'Ortega', 3,2),
(55667788, 'Laura', 'Vega', 4, 4),
(66778899, 'Ramón', 'Ruiz', 5, 5),
(77889900, 'Teresa', 'Muñoz', 6, 6),
(88990011, 'Raúl', 'Castro', 7, 7),
(99001122, 'Inés', 'Núñez', 8, 8),
(10012233, 'Felipe', 'Mendoza', 9, 9),
(11023344, 'Mariana', 'Ríos', 10, 10);

-- Insertar registros en la tabla cursada
INSERT INTO cursada (id_cursada, curso, instructor, alumnos) VALUES 
(1, 1, 22334455, 12345678),
(2, 2, 33445566, 23456789),
(3, 3, 44556677, 34567890),
(4, 4, 55667788, 45678901),
(5, 5, 66778899, 56789012),
(6, 6, 77889900, 67890123),
(7, 7, 88990011, 78901234),
(8, 8, 99001122, 89012345),
(9, 9, 10012233, 90123456),
(10, 10, 11023344, 12340987);


