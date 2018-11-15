delimiter |

CREATE TRIGGER process_definitions_bu
  BEFORE UPDATE ON process_definitions
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

