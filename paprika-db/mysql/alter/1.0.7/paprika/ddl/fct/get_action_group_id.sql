delimiter |

CREATE FUNCTION get_action_group_id (p_name varchar(255)) RETURNS int(11)
BEGIN
	DECLARE l_result int(11);
  SELECT id INTO l_result FROM action_groups WHERE name=p_name;
  RETURN l_result;
END;
|
delimiter ;