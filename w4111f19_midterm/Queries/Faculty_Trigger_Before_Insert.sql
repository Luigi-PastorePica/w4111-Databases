CREATE DEFINER = `dbuser`@`localhost` TRIGGER `collegemodel`.`faculty_BEFORE_INSERT` BEFORE INSERT ON `faculty` FOR EACH ROW
BEGIN
	SET NEW.uni = generate_uni(NEW.first_name, NEW.last_name);
END
