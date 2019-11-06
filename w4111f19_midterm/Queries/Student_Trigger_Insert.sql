CREATE DEFINER = `root`@`localhost` TRIGGER `collegemodel`.`student_BEFORE_UPDATE` BEFORE UPDATE ON `student` FOR EACH ROW
BEGIN
	IF NEW.student != OLD.student THEN
        SIGNAL SQLSTATE '45002'
            SET MESSAGE_TEXT="UNI is immutable";
    END IF;

END