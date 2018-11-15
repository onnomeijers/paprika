delimiter |

CREATE TRIGGER processes_properties_bi
  BEFORE INSERT ON processes_properties
    FOR EACH ROW BEGIN
      SET NEW.created_at=NOW();
      SET NEW.created_by=CURRENT_USER();
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

