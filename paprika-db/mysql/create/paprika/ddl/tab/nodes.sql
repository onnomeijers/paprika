CREATE TABLE nodes
(
  id                int(11) not null auto_increment primary key,
  name              varchar(100) not null,
  value             varchar(4000) not null,
  hashcode          varchar(255),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);