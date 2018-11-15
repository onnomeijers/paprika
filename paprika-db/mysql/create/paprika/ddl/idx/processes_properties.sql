CREATE INDEX ppy_pcs_id_idx ON processes_properties (pcs_id);
CREATE INDEX ppy_name_idx ON processes_properties (name);
CREATE INDEX ppy_pan_id_name_idx ON processes_properties (pcs_id, name);