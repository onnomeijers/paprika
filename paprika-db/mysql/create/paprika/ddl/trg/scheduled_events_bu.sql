delimiter |

CREATE TRIGGER scheduled_events_bu
  BEFORE UPDATE ON scheduled_events
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

