ALTER TABLE files ADD CONSTRAINT fle_pcs_fk FOREIGN KEY (pcs_id) REFERENCES processes (id);
ALTER TABLE files ADD CONSTRAINT fle_rle_fk FOREIGN KEY (rle_id) REFERENCES rules (id);