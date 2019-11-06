CREATE DEFINER=`root`@`localhost` FUNCTION `generate_uni` (first_name VARCHAR(64), last_name VARCHAR(64))
RETURNS VARCHAR(12) CHARSET utf8 DETERMINISTIC
BEGIN
	DECLARE first_prefix VARCHAR(2);
    DECLARE last_prefix VARCHAR(2);
    DECLARE prefix_count INT;
    DECLARE full_prefix VARCHAR(5);
    DECLARE	result VARCHAR(12);
    
    SET first_prefix = LOWER(SUBSTR(first_name, 1, 2)); 
    SET last_prefix = LOWER(SUBSTR(last_name, 1, 2));
    SET full_prefix = CONCAT(first_prefix, last_prefix, '%');
    SET prefix_count = (SELECT COUNT(*) AS count FROM people where UNI LIKE (full_prefix));
    SET result = CONCAT(first_prefix, last_prefix, prefix_count + 1);
    
	RETURN result;
END
