ALTER TABLE triggers DROP type;
ALTER TABLE triggers DROP payload;
ALTER TABLE triggers DROP INDEX name;
alter table triggers add active int(1) not null default 1;
alter table triggers add tte_id int(11);
alter table triggers add datasource varchar(255);
alter table triggers add selector varchar(4000);
alter table triggers add updater varchar(4000);
alter table triggers add options varchar(4000);
alter table triggers add repetition varchar(255);
alter table triggers add intermission int(11);
alter table triggers add expected datetime;
alter table triggers add url varchar(255);
alter table triggers add patterns varchar(255);
alter table triggers add recursive int(1);
alter table triggers add depth int(1);
alter table triggers add username varchar(255);
alter table triggers add password varchar(255);