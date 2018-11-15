delimiter |

CREATE TRIGGER file_properties_bu
  BEFORE UPDATE ON file_properties
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

