alter table user_roles add constraint ure_usr_fk FOREIGN KEY (usr_id) REFERENCES users (id);
alter table user_roles add constraint ure_roe_fk FOREIGN KEY (roe_id) REFERENCES roles (id);