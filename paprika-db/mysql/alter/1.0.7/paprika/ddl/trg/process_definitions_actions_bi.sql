drop trigger process_definitions_actions_bi;
delimiter |

CREATE TRIGGER process_definitions_actions_bi
  BEFORE INSERT ON process_definitions_actions
    FOR EACH ROW BEGIN
      DECLARE hash VARCHAR(255);
      declare id int default 0;

      select auto_increment into id
        from information_schema.tables
       where table_name = 'process_definitions_actions'
         and table_schema = database();

      SELECT MD5(CONCAT(RAND(), NOW())) INTO hash;
	  SET NEW.created_at=NOW();
      SET NEW.created_by=CURRENT_USER();
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
      SET NEW.hashcode=hash;

      if new.origin is null then
        SET NEW.origin=get_property('origin');
      end if;

      if new.id_ is null then
        SET new.id_=id;
      end if;
    END;
|

delimiter ;

