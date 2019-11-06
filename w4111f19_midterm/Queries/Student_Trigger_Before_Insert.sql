CREATE DEFINER = `dbuser`@`localhost` TRIGGER `collegemodel`.`student_BEFORE_INSERT` BEFORE INSERT ON `student` FOR EACH ROW
BEGIN
	set new.student = generate_uni(new.first_name, new.last_name);
END
