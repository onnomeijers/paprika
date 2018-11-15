ALTER TABLE rules ADD CONSTRAINT rle_lcn_fk FOREIGN KEY (lcn_id) REFERENCES locations (id);
ALTER TABLE rules ADD CONSTRAINT rle_hok_fk FOREIGN KEY (hok_id) REFERENCES hooks (id);
ALTER TABLE rules ADD CONSTRAINT rle_stm_fk FOREIGN KEY (stm_id) REFERENCES streams (id);
ALTER TABLE rules ADD CONSTRAINT rle_pdn_fk FOREIGN KEY (pdn_id) REFERENCES process_definitions (id);
ALTER TABLE rules ADD CONSTRAINT rle_e_pdn_fk FOREIGN KEY (e_pdn_id) REFERENCES process_definitions (id);