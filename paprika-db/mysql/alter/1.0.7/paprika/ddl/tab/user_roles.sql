CREATE TABLE user_roles
(
  id           int(11) not null AUTO_INCREMENT primary key,
  hashcode     varchar(255),
  usr_id       int(11) not null,
  roe_id       int(11) not null,
  active       int(1) not null default 1,
  created_at   datetime,
  created_by   varchar(45),
  updated_at   datetime,
  updated_by   varchar(45)
);