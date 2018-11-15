delimiter |

CREATE TRIGGER pipelines_bu
  BEFORE UPDATE ON pipelines
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

