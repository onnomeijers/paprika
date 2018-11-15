delimiter |

CREATE TRIGGER activations_bu
  BEFORE UPDATE ON activations
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

