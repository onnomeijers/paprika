delimiter |

CREATE FUNCTION get_role_id (p_name VARCHAR(255)) RETURNS VARCHAR(255)
BEGIN
	DECLARE l_result VARCHAR(255);
  SELECT id INTO l_result FROM roles WHERE name=p_name;
  RETURN l_result;
END;
|
delimiter ;