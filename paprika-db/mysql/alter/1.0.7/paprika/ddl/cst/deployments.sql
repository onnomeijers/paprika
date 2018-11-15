alter table deployments add constraint dpt_tgr_fk FOREIGN KEY (tgr_id) REFERENCES triggers (id);
alter table deployments add constraint dpt_flw_fk FOREIGN KEY (flw_id) REFERENCES flows (id);
alter table deployments add constraint dpt_e_flw_fk FOREIGN KEY (e_flw_id) REFERENCES flows (id);