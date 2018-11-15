CREATE TABLE processes
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  job_name          varchar(255),
  pdn_id            int(11),
  e_pdn_id          int(11),
  hashcode          varchar(255),
  name              varchar(255),
  queue             varchar(255),
  state             varchar(50),
  message           varchar(4000),
  backtrace         varchar(4000),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);