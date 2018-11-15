delimiter |

CREATE TRIGGER recursives_bi
  BEFORE INSERT ON recursives
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
      SET NEW.hashcode=hash;
    END;
|

delimiter ;

