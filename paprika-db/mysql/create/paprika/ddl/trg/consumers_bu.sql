delimiter |

CREATE TRIGGER consumers_bu
  BEFORE UPDATE ON consumers
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

