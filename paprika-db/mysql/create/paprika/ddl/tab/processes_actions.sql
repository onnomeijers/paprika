CREATE TABLE processes_actions
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  job_name          varchar(255),
  name              varchar(255),
  hashcode          varchar(255),
  pcs_id            int(11),
  dan_id            int(11),
  state             varchar(50),
  message           varchar(4000),
  backtrace         varchar(4000),
  active            int(1) NOT NULL DEFAULT 1,
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);