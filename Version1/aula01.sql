-- -----------------------------------------------------
-- Database aula
-- -----------------------------------------------------
CREATE DATABASE IF NOT EXISTS `aula01` ;
USE `aula01` ;

-- -----------------------------------------------------
-- Table `aula`.`direccion' del alumno
-- -----------------------------------------------------

CREATE TABLE direccion (
  id INT(11) NOT NULL PRIMARY KEY,
  calle VARCHAR(32),
  numero INT(11) NOT NULL,
  codigoP INT(11) NOT NULL
);

-- -----------------------------------------------------
-- Table `aula`.`direccion' del Instructor
-- -----------------------------------------------------

CREATE TABLE mensajes (
  id_mensaje INT(11) NOT NULL PRIMARY KEY,
  mensaje VARCHAR(30)
 );

-- -----------------------------------------------------
-- Table `aula`.`educacion' del alumno
-- -----------------------------------------------------

CREATE TABLE educacion (
  id_educacion INT PRIMARY KEY,
  educacionMax VARCHAR(30) NOT NULL,
  institucion VARCHAR(80) NOT NULL,
  titulo VARCHAR(30) NOT NULL
);

-- -----------------------------------------------------
-- Table `aula`.`educacion' del Instructor
-- -----------------------------------------------------

CREATE TABLE educacionInst (
  id_educacion INT PRIMARY KEY,
  educacionMax VARCHAR(30) NOT NULL,
  institucion VARCHAR(80) NOT NULL,
  titulo VARCHAR(30) NOT NULL
);

-- -----------------------------------------------------
-- Table `aula`.`cursos`
-- -----------------------------------------------------
CREATE TABLE cursos (
  codigo INT(11) NOT NULL PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  descripcion VARCHAR(45)
);

-- -----------------------------------------------------
-- Table `aula`.`alumnos`
-- -----------------------------------------------------
CREATE TABLE alumnos (
  dni INT(11) NOT NULL PRIMARY KEY,
  nombre VARCHAR(20) NOT NULL,
  apellido VARCHAR(20) NOT NULL,
  direccion INT(5),
  educacion INT(5),
  FOREIGN KEY(direccion) REFERENCES direccion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY(educacion) REFERENCES educacion(id_educacion)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- -----------------------------------------------------
-- Table `aula`.`instructores`
-- -----------------------------------------------------
CREATE TABLE instructores (
  dni INT(11) NOT NULL PRIMARY KEY,
  nombre VARCHAR(20) NOT NULL,
  apellido VARCHAR(20) NOT NULL,
  direccion INT(5),
  educacion INT(5),
  -- cursos INT(11),
  FOREIGN KEY(direccion) REFERENCES direccion(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY(educacion) REFERENCES educacionInst(id_educacion)
    ON DELETE CASCADE
    ON UPDATE CASCADE
  -- FOREIGN KEY(cursos) REFERENCES cursos(codigo)
    -- ON DELETE CASCADE
   -- ON UPDATE CASCADE
);

-- -----------------------------------------------------
-- Table `aula`.`cursada'
-- -----------------------------------------------------
CREATE TABLE cursada (
  id_cursada INT(11) NOT NULL PRIMARY KEY,
  curso INT(11) NOT NULL,
  instructor INT(11) NOT NULL,
  alumnos INT(11) NOT NULL,
  FOREIGN KEY(curso) REFERENCES cursos(codigo)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY(instructor) REFERENCES instructores(dni)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY(alumnos) REFERENCES alumnos(dni)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- -----------------------------------------------------
-- Table `aula`.`users'
-- -----------------------------------------------------


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

-- ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';
