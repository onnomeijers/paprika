delimiter |

CREATE TRIGGER processes_actions_properties_bu
  BEFORE UPDATE ON processes_actions_properties
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

