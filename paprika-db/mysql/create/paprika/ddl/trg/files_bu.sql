delimiter |

CREATE TRIGGER files_bu
  BEFORE UPDATE ON files
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

