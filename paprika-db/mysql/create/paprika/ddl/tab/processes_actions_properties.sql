CREATE TABLE processes_actions_properties
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  name              varchar(255),
  value             varchar(255),
  pan_id            int(11),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);