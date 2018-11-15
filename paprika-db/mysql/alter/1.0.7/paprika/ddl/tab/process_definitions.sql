alter table process_definitions add id_ int(11);
alter table process_definitions add active int(1) not null default 1;
alter table process_definitions add changed int(1) not null default 1;
alter table process_definitions add origin varchar(255);
alter table process_definitions add target varchar(255);
