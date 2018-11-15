CREATE TABLE flows
(
  id                int(11) not null auto_increment primary key,
  name              varchar(100) not null,
  description       varchar(4000),
  payload           varchar(4000) not null,
  active            int(1) not null default 1,
  hashcode          varchar(255),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);