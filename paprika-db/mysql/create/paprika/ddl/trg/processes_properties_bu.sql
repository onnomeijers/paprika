delimiter |

CREATE TRIGGER processes_properties_bu
  BEFORE UPDATE ON processes_properties
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

