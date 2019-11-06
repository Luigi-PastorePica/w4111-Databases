-- CREATE DATABASE collegemodel;
USE collegemodel;

CREATE TABLE `student` (
  `student` varchar(12) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `graduation_year` year(4) NOT NULL,
  PRIMARY KEY (`student`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `faculty` (
  `uni` varchar(12) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `title` enum('Professor','Assistant Professor','Associate Professor','Adjunct Professor') NOT NULL,
  PRIMARY KEY (`uni`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE VIEW people AS
	SELECT UNI, last_name, first_name, 'S' AS person_type, graduation_year, 'NA' AS title
    FROM student
    UNION
    SELECT UNI, last_name, first_name, 'F' AS person_type, 'NA' AS graduation_year, title
    FROM FACULTY;