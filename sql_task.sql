CREATE TABLE TABLE_A (
	trainerid INT,
	starttime timestamp,
	endtime timestamp
);

insert into table_a
values (1234, '2018-10-01 08:30', '2018-10-01 09:00'),
(1234,'2018-10-01 08:45:00','2018-10-01 09:15:00'),
(1234, '2018-10-01 09:30:00',	'2018-10-01 10:00:00'),
(2345, '2018-10-01 08:45:00',	'2018-10-01 09:15:00'),
(2345, '2018-10-01 09:30:00',	'2018-10-01 10:00:00'),
(2345, '2018-10-01 10:50:00',	'2018-10-01 11:00:00'),
(2345, '2018-10-01 09:50:00',	'2018-10-01 10:00:00');

create index idx on table_a(trainerid, starttime asc, endtime);
create index reverse_idx on table_a(trainerid, starttime, endtime desc);

with main as (
	select
		trainerid,
		starttime,
		endtime,
		lag (endtime, 1)
			over
			(partition by trainerid order by starttime) as prev_end
	from table_a
	)
select * from main where
starttime < prev_end;


