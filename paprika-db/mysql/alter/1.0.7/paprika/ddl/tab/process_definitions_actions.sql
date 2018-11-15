alter table process_definitions_actions add id_ int(11);
alter table process_definitions_actions add changed int(1) not null default 1;
alter table process_definitions_actions add origin varchar(255);
alter table process_definitions_actions add target varchar(255);
