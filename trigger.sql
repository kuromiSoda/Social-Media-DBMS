-- check the age 
DELIMITER $$
CREATE TRIGGER user_bi 
BEFORE INSERT
ON USERS
FOR EACH ROW
IF NEW.age < 18 THEN
    SIGNAL SQLSTATE '50001' 
    SET MESSAGE_TEXT = 'Person must be older than 18.';
END IF; 
$$ DELIMITER;


