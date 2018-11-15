delimiter |

CREATE TRIGGER nodes_bu
  BEFORE UPDATE ON nodes
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

