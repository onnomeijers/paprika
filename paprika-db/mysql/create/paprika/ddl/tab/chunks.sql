CREATE TABLE chunks
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  job_name          varchar(255),
  pcs_id            int(11),
  state             varchar(50),
  datasource        varchar(255),
  tablename         varchar(255),
  selector          varchar(4000),
  options           varchar(4000),
  payload           varchar(4000),
  message           varchar(4000),
  backtrace         varchar(4000),
  rle_id            int(11),
  rule              varchar(50),
  pattern           varchar(4000),
  hashcode          varchar(255),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);