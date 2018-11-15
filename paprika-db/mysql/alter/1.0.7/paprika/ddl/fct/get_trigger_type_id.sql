delimiter |

CREATE FUNCTION get_trigger_type_id (p_name varchar(255)) RETURNS int(11)
BEGIN
	DECLARE l_result int(11);
  SELECT id INTO l_result FROM trigger_types WHERE name=p_name;
  RETURN l_result;
END;
|
delimiter ;