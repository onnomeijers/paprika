delimiter |

CREATE TRIGGER triggers_bu
  BEFORE UPDATE ON triggers
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;
