delimiter |

CREATE TRIGGER deployments_bi
  BEFORE INSERT ON deployments
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
      SET NEW.hashcode=hash;
    END;
|

delimiter ;

