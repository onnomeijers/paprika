delimiter |

CREATE FUNCTION get_user_id (p_username VARCHAR(255)) RETURNS VARCHAR(255)
BEGIN
	DECLARE l_result VARCHAR(255);
  SELECT id INTO l_result FROM users WHERE username=p_username;
  RETURN l_result;
END;
|
delimiter ;