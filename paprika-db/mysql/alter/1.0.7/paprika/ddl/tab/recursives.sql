CREATE TABLE recursives
(
  id           int not null auto_increment primary key,
  name         varchar(255) not null,
  value        int(1) not null,
  hashcode     varchar(255),
  active       int(1) not null default 1,
  created_at   datetime not null,
  created_by   varchar(45) not null,
  updated_at   datetime not null,
  updated_by   varchar(45) not null
);