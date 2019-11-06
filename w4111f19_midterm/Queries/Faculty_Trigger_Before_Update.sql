CREATE DEFINER = `dbuser`@`localhost` TRIGGER `collegemodel`.`faculty_BEFORE_UPDATE` BEFORE UPDATE ON `faculty` FOR EACH ROW
BEGIN
	IF NEW.uni != OLD.uni THEN 
        SIGNAL SQLSTATE '45002'
            SET MESSAGE_TEXT="UNI is immutable";
    END IF;
END
