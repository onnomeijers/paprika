CREATE TABLE files
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  job_name          varchar(255),
  pcs_id            int(11),
  filename          varchar(255),
  path              varchar(255),
  pattern           varchar(255),
  filesize          int(11),
  pickup_location   varchar(4000),
  state             varchar(50),
  message           varchar(4000),
  backtrace         varchar(4000),
  rle_id            int(11),
  rule              varchar(50),
  hashcode          varchar(255),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);