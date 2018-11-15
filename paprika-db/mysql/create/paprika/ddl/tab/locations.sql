CREATE TABLE locations
(
  id          int(11) NOT NULL AUTO_INCREMENT primary key,
  name        varchar(255),
  hashcode    varchar(255),
  url         varchar(4000) NOT NULL,
  patterns    varchar(4000),
  recursive   int(1) DEFAULT 0 not null,
  depth       int(1) DEFAULT -1 not null,
  active      int(1) NOT NULL DEFAULT 1,
  created_at  datetime,
  created_by  varchar(45),
  updated_at  datetime,
  updated_by  varchar(45)
);
