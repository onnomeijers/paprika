CREATE TABLE scheduled_events
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  name              varchar(255),
  hashcode          varchar(255),
  repetition        varchar(255) NOT NULL,
  intermission      int(11) DEFAULT 1,
  expected          datetime,
  active            int(1) NOT NULL DEFAULT 1,
  pdn_id            int(11),
  e_pdn_id          int(11),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);