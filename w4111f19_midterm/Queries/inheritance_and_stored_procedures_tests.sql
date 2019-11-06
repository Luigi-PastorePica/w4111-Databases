USE collegemodel;

SELECT * FROM people;

CALL collegemodel.insert_new_person('lap2204', 'Pastore Pica', 'Luigi', 'S', '2020', null);

SELECT * FROM student;
set sql_safe_updates=0;
UPDATE collegemodel.student set student='lap2204' WHERE first_name='Luigi'; -- this should return an error.

CALL collegemodel.insert_new_person('lap2204', 'Pascuarielli', 'Lucca', 'F', null , 'Assistant Professor');

SELECT * FROM faculty;

UPDATE collegemodel.faculty set faculty='lap2204' WHERE first_name='Lucca'; -- this should return an error.alter

CALL collegemodel.insert_new_person('lap2204', 'Pastorelli', 'Lucciano', 'P', null , 'Associate Professor'); -- This should return an error

CALL collegemodel.insert_new_person('lap2204', 'Pastorelli', 'Lucciano', 'F', 2011 , 'Associate Professor');

SELECT * FROM faculty;

CALL collegemodel.insert_new_person('lap2204', 'Pazzo', 'Ludomenico', 'S', 2011 , 'Associate Professor');

SELECT * FROM student;

SELECT * FROM people;

-- This deletes every entry in both tables
DELETE FROM student WHERE student LIKE 'lupa%';
DELETE FROM faculty WHERE uni LIKE 'lupa%';