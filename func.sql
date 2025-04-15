-- function to count number of comments per post

DELIMITER $$
CREATE FUNCTION noc(P_ID INT) 
RETURNS INT
DETERMINISTIC
BEGIN
    declare c INT;
    set c = (SELECT count(*) from post_comments WHERE post_comments.Post_ID = P_ID);
    RETURN c;
END
$$ 
DELIMITER;

--  function to count the number of posts a user has

DELIMITER $$
CREATE FUNCTION nop(uid INT)
returns INT
DETERMINISTIC
BEGIN
	Declare c INT;
	set c = (Select count(*) from posts where Posted_User_ID=uid);
	return c;
END
$$
DELIMITER ;

