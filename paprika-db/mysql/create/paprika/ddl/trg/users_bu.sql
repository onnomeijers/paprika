delimiter |

CREATE TRIGGER users_bu
  BEFORE UPDATE ON users
    FOR EACH ROW BEGIN
      if (new.password) then
        SET NEW.password=MD5(new.password);
      end if;
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

