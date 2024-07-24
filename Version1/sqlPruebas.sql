select instructores.dni, instructores.nombre, cursada.instructor  from instructores,cursada where cursada.instructor = instructores.dni and instructores.dni = 33445566;

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

INSERT INTO cursada (id_cursada, curso, instructor, alumnos) VALUES 
(1, 1, 22334455, 12340987),
(1, 1, 22334455, 23456789),
(1, 1, 22334455, 34567890),
(1, 1, 22334455, 45678901);

 UPDATE `cursada`
        SET curso = 2, instructor = 11023344, alumnos = 89012345
         WHERE cursada.id_cursada = 14;
         
select instructores.dni, instructores.nombre, instructores.apellido  from instructores,cursada  where instructores.dni= cursada.instructor and  cursada.id_cursada = 5;

SELECT (MAX(id_cursada)+1) AS max_id_cursada FROM cursada;

select * from cursada;

select * from mensajes where id_mensaje =1;

SELECT 
    cursada.id_cursada,
    cursos.codigo,
    cursos.nombre AS curso_nombre,
    alumnos.dni AS alumno_dni,
    alumnos.nombre AS alumno_nombre,
    alumnos.apellido AS alumno_apellido,
    instructores.dni AS instructor_dni,
    instructores.nombre AS instructor_nombre,
    instructores.apellido AS instructor_apellido
FROM 
    cursada
JOIN 
    cursos ON cursada.curso = cursos.codigo
JOIN 
    alumnos ON cursada.alumnos = alumnos.dni
JOIN 
    instructores ON cursada.instructor = instructores.dni
WHERE 
    cursada.id_cursada = 3;  -- Reemplaza ? con el id_cursada que deseas consultar
    
    
SELECT 
    cursada.id_cursada,
    cursos.codigo,
    cursos.nombre AS curso_nombre,
    alumnos.dni AS alumno_dni,
    alumnos.nombre AS alumno_nombre,
    alumnos.apellido AS alumno_apellido,
    instructores.dni AS instructor_dni,
    instructores.nombre AS instructor_nombre,
    instructores.apellido AS instructor_apellido
FROM 
    cursada
JOIN 
    cursos ON cursada.curso = cursos.codigo
JOIN 
    alumnos ON cursada.alumnos = alumnos.dni
JOIN 
    instructores ON cursada.instructor = instructores.dni
ORDER BY 
    cursada.id_cursada;

SELECT * FROM users WHERE username = "Campitos";

ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';

SELECT * FROM users;

select * from users where id = 2;


