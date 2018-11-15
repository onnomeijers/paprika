CREATE TABLE streams
(
  id           int(11) NOT NULL AUTO_INCREMENT primary key,
  name         varchar(255),
  hashcode     varchar(255),
  url          varchar(4000) NOT NULL,
  username     varchar(255) NOT NULL,
  password     varchar(255) NOT NULL,
  active       int(1) NOT NULL DEFAULT 1,
  created_at   datetime,
  created_by   varchar(45),
  updated_at   datetime,
  updated_by   varchar(45)
);