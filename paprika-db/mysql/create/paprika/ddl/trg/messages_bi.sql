delimiter |

CREATE TRIGGER messages_bi
  BEFORE INSERT ON messages
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
      IF (NEW.delay is null) then
        SET NEW.delay=NOW();
      END IF;
	  SET NEW.created_at=NOW();
      SET NEW.created_by=CURRENT_USER();
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
      SET NEW.hashcode=hash;
    END;
|

delimiter ;

