CREATE TABLE process_definitions
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  hashcode          varchar(255),
  name              varchar(255),
  queue             varchar(255) default 'messages',
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);