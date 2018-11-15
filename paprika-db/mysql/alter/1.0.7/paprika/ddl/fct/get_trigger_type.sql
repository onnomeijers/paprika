delimiter |

CREATE FUNCTION get_trigger_type (p_id int(11)) RETURNS VARCHAR(255)
BEGIN
	DECLARE l_result VARCHAR(255);
  SELECT name INTO l_result FROM trigger_types WHERE id=p_id;
  RETURN l_result;
END;
|
delimiter ;