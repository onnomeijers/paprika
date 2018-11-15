CREATE TABLE triggers
(
  id           int not null auto_increment primary key,
  name         varchar(100) not null unique,
  type         varchar(255),
  hashcode     varchar(255),
  payload      varchar(4000) not null,
  description  varchar(255),
  created_at   datetime not null,
  created_by   varchar(45) not null,
  updated_at   datetime not null,
  updated_by   varchar(45) not null
);