delimiter |

CREATE TRIGGER actions_bu
  BEFORE UPDATE ON actions
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

