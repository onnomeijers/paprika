CREATE TABLE rules
(
  id               int(11) NOT NULL AUTO_INCREMENT primary key,
  lcn_id           int(11),
  hok_id           int(11),
  stm_id           int(11),
  rule             varchar(50),
  pattern          varchar(4000),
  pdn_id           int(11),
  e_pdn_id         int(11),
  active           int(1) NOT NULL DEFAULT 1,
  created_at       datetime,
  created_by       varchar(45),
  updated_at       datetime,
  updated_by       varchar(45)
);