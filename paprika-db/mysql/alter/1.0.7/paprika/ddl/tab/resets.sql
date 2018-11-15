CREATE TABLE resets
(
  id           int not null auto_increment primary key,
  username     varchar(255) not null,
  hashkey      varchar(255) not null,
  active       int(1) not null default 1,
  used         int(1) not null default 0,
  created_at   datetime not null,
  created_by   varchar(45) not null,
  updated_at   datetime not null,
  updated_by   varchar(45) not null
);