CREATE TABLE events
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  job_name          varchar(255),
  state             varchar(50),
  message           varchar(4000),
  backtrace         varchar(4000),
  repetition        varchar(255) NOT NULL,
  intermission      int(11) DEFAULT 1,
  pcs_id            int(11),
  hashcode          varchar(255),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);