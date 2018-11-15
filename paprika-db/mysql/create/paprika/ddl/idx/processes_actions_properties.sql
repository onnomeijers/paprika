CREATE INDEX pay_pan_id_idx ON processes_actions_properties (pan_id);
CREATE INDEX pay_name_idx ON processes_actions_properties (name);
CREATE INDEX pay_pan_id_name_idx ON processes_actions_properties (pan_id, name);