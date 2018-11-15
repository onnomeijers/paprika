delimiter |

CREATE TRIGGER trigger_types_bi
  BEFORE INSERT ON trigger_types
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
      SET NEW.hashcode=hash;
    END;
|

delimiter ;

