delimiter |

CREATE FUNCTION get_process_definition_action_id (p_process_name VARCHAR(255), p_name VARCHAR(255)) RETURNS VARCHAR(255)
BEGIN
  DECLARE l_result VARCHAR(255);
  SELECT id INTO l_result FROM process_definitions_actions WHERE name=p_name and pdn_id=get_process_definition_id(p_process_name);
  RETURN l_result;
END;
|
delimiter ;