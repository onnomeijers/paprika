delimiter |

CREATE TRIGGER rules_bu
  BEFORE UPDATE ON rules
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

