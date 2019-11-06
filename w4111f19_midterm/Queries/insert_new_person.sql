CREATE PROCEDURE `insert_new_person` (uni VARCHAR(12), last_name VARCHAR(64), first_name VARCHAR(64), person_type VARCHAR(1), graduation_year YEAR(4), title VARCHAR(20))
BEGIN
	IF person_type='S' THEN
		INSERT INTO student (student, last_name, first_name, graduation_year) VALUES(uni, last_name, first_name, graduation_year);
	ELSEIF person_type='F' THEN
		INSERT INTO faculty (uni, last_name, first_name, title) VALUES(uni, last_name, first_name, title);
	ELSE
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Cannot insert person. Invalid value for person_type. person_type can only be S or F';
		-- SIGNAL idea source: http://www.mysqltutorial.org/mysql-signal-resignal/
	END IF;
END