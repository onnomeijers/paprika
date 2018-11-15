delimiter |

CREATE TRIGGER processes_actions_bi
  BEFORE INSERT ON processes_actions
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
      SET NEW.created_at=NOW();
      SET NEW.created_by=CURRENT_USER();
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
      SET NEW.hashcode=hash;
    END;
|

delimiter ;

