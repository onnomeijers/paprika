CREATE TABLE action_groups
(
  id           int not null auto_increment primary key,
  name         varchar(255),
  tte_id       int(11),
  icon         varchar(255),
  active       int(1) not null default 1,
  created_at   datetime not null,
  created_by   varchar(45) not null,
  updated_at   datetime not null,
  updated_by   varchar(45) not null
);