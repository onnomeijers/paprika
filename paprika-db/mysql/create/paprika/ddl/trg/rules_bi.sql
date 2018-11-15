delimiter |

CREATE TRIGGER rules_bi BEFORE INSERT ON rules
  FOR EACH ROW BEGIN
	SET NEW.created_at=NOW();
    SET NEW.created_by=CURRENT_USER();
    SET NEW.updated_at=NOW();
    SET NEW.updated_by=CURRENT_USER();
  END;
|

delimiter ;