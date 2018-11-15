CREATE TABLE file_properties
(
  id           int not null auto_increment primary key,
  fle_id       int(11) not null,
  name         varchar(100) not null,
  value        varchar(4000) not null,
  created_at   datetime,
  created_by   varchar(45),
  updated_at   datetime,
  updated_by   varchar(45)
)