CREATE INDEX apy_dan_id_idx ON process_definitions_actions_properties (dan_id);
CREATE INDEX apy_name_idx ON process_definitions_actions_properties (name);
CREATE INDEX apy_dan_id_name_idx ON process_definitions_actions_properties (dan_id, name);