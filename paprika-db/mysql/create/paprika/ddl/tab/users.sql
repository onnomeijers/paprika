CREATE TABLE users
(
  id           int(11) NOT NULL AUTO_INCREMENT primary key,
  hashcode     varchar(255),
  username     varchar(255) NOT NULL,
  password     varchar(255) NOT NULL,
  name         varchar(255),
  nickname     varchar(255),
  organization varchar(255),
  active       int(1) NOT NULL DEFAULT 1,
  created_at   datetime,
  created_by   varchar(45),
  updated_at   datetime,
  updated_by   varchar(45)
);