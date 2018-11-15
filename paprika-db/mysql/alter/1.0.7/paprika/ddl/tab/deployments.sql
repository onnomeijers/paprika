CREATE TABLE deployments
(
  id           int not null auto_increment primary key,
  name         varchar(255) not null,
  hashcode     varchar(255),
  tgr_id       int(11),
  pattern      varchar(255),
  flw_id       int(11),
  e_flw_id     int(11),
  active       int(1) not null default 1,
  created_at   datetime not null,
  created_by   varchar(45) not null,
  updated_at   datetime not null,
  updated_by   varchar(45) not null
);