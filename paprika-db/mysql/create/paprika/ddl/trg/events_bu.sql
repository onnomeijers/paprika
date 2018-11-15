delimiter |

CREATE TRIGGER events_bu
  BEFORE UPDATE ON events
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

