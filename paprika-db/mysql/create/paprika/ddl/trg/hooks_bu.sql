delimiter |

CREATE TRIGGER hooks_bu
  BEFORE UPDATE ON hooks
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

