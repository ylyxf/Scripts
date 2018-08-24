SELECT
       COUNT(DISTINCT "Task Status History Cts Created Component"."task_id") AS "Count of distinct Task Id"
FROM "public"."task_status_history__cts__verified_component" AS "Task Status History Cts Created Component"
WHERE (("Task Status History Cts Created Component"."ts" AT TIME ZONE 'UTC') BETWEEN CURRENT_TIMESTAMP - INTERVAL '120 DAY' AND CURRENT_TIMESTAMP)

LIMIT 10000;

select task_id, username, ts
from task_status_history__cts__verified_component as "verified"
where ((verified.ts AT TIME ZONE 'UTC') BETWEEN CURRENT_TIMESTAMP - INTERVAL '170 DAY' AND CURRENT_TIMESTAMP) ;


select verified.component_id, verified.ts, verified.task_id from 
(
	select *, (row_number() over(partition by task_id order by ts)) 
	Row_Num 
	from task_status_history__cts__verified_component
) verified
where verified.Row_Num=1
and (verified.ts at time zone 'UTC') > '2017-04-01' 
order by verified.ts;




select c.component_id, c.factors__component_id, c.complexity_score, c.factors__num_pins, c.factors__generator_used, 
c.factors__has_polygon_in_footprint, c.factors__prefix
from component_complexity c
inner join 

  (**replace with component id) t
  
on t.component_id = c.component_id;




select m.component_id, m.manufacturers from component_complexity__factors__manufacturers m
inner join 

	(**replace with component id) t

on t.component_id = m.component_id;




select e.component_id, sum(e.quantity) from component_complexity__factors__thing_enumeration e
inner join

(**replace with component id) t

on t.component_id = e.component_id
group by e.component_id;


select * from task_statuses__assigned where task_id='0009e3f5dec75d4b'
select * from task_statuses__skipped where task_id='361fd7e4a135531a'


select s.task_id, count(s.username) from task_statuses__cts__rejected_verified s
inner join 
(
	select verified.component_id, verified.ts, verified.task_id from 
		(
			select *, (row_number() over(partition by task_id order by ts)) Row_Num 
			from task_status_history__cts__verified_component
		) verified
	where verified.Row_Num=1
	and (verified.ts at time zone 'UTC') > '2017-04-01' 
	order by verified.ts
) t
on s.task_id = t.task_id
group by s.task_id;
