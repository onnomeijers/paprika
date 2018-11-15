delimiter |

CREATE TRIGGER repetitions_bi
  BEFORE INSERT ON repetitions
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
      SET NEW.hashcode=hash;
    END;
|

delimiter ;

