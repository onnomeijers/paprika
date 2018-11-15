delimiter |

CREATE FUNCTION get_hook_id (p_datasource VARCHAR(255), p_tablename VARCHAR(255)) RETURNS VARCHAR(255)
BEGIN
	DECLARE l_result VARCHAR(255);
  SELECT id INTO l_result FROM hooks WHERE datasource=p_datasource and tablename=p_tablename;
  RETURN l_result;
END;
|
delimiter ;