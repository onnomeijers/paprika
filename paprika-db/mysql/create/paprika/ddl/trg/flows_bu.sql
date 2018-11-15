delimiter |

CREATE TRIGGER flows_bu
  BEFORE UPDATE ON flows
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

