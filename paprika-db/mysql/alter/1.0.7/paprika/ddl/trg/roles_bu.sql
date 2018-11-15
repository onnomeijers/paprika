delimiter |

CREATE TRIGGER roles_bu
  BEFORE UPDATE ON roles
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

