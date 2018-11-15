delimiter |

CREATE TRIGGER streams_bu
  BEFORE UPDATE ON streams
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

