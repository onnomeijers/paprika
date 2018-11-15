ALTER TABLE chunks ADD CONSTRAINT chk_pcs_fk FOREIGN KEY (pcs_id) REFERENCES processes (id);
ALTER TABLE chunks ADD CONSTRAINT chk_rle_fk FOREIGN KEY (rle_id) REFERENCES rules (id);