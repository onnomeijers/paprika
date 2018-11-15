delimiter |

CREATE TRIGGER process_definitions_actions_properties_bu
  BEFORE UPDATE ON process_definitions_actions_properties
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

