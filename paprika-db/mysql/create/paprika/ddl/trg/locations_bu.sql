delimiter |

CREATE TRIGGER locations_bu
  BEFORE UPDATE ON locations
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

