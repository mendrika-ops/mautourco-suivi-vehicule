

create or replace view suivivehicule_statuspos_min as 
SELECT 1 as id, 
ss.id_trip, 
MIN(ss.daty_time) AS daty_time, 
MIN(ss.duration) AS duration, 
MIN(ss.distance) AS distance, 
ss.is_call_api ,
ss.uid
FROM suivivehicule_statusposdetail ss
join suivivehicule_units su on su.uid = ss.uid
GROUP BY ss.id_trip, ss.is_call_api, ss.uid;

create or replace view suivivehicule_statuspos_bank_notin_record as 
SELECT sb.id_trip, sb.daty_time, sb.speed, sb.speedMeasure, sb.odometer, sb.ignition, sb.engineTime, sb.engineStatus 
FROM suivivehicule_bankposition sb
LEFT JOIN suivivehicule_recordcomment sr ON sb.id_trip = sr.id_trip
WHERE sr.id_trip IS NULL;

-- completed count 794
create or replace view suivivehicule_statuspos_min_cplt as 
select 
1 as id,
ssm.id_trip,
ssm.daty_time,
ssm.duration,
ssm.distance,
ssm.is_call_api,
ssm.uid,
ssbnr.speed,
ssbnr.speedMeasure,
ssbnr.odometer,
ssbnr.ignition,
ssbnr.engineTime,
ssbnr.engineStatus
from suivivehicule_statuspos_min ssm
	join suivivehicule_statuspos_bank_notin_record ssbnr on ssm.id_trip = ssbnr.id_trip 
	where ssm.duration <= 200 

-- in transit count 2 940
create or replace view suivivehicule_statuspos_min_transit as 
select 
1 as id,
ssm.id_trip,
ssm.daty_time,
ssm.duration,
ssm.distance,
ssm.is_call_api,
ssm.uid,
ssbnr.speed,
ssbnr.speedMeasure,
ssbnr.odometer,
ssbnr.ignition,
ssbnr.engineTime,
ssbnr.engineStatus
from suivivehicule_statuspos_min ssm
	join suivivehicule_statuspos_bank_notin_record ssbnr on ssm.id_trip = ssbnr.id_trip 
	where ssbnr.engineStatus like 'in transit%' and ssbnr.ignition = 'on' and ssm.duration > 200 
	
-- in transit igniton off count 12
	
select 
ssm.id_trip,
ssm.daty_time,
ssm.duration,
ssm.distance,
ssm.is_call_api,
ssm.uid,
ssbnr.speed,
ssbnr.speedMeasure,
ssbnr.odometer,
ssbnr.ignition,
ssbnr.engineTime,
ssbnr.engineStatus
from suivivehicule_statuspos_min ssm
	join suivivehicule_statuspos_bank_notin_record ssbnr on ssm.id_trip = ssbnr.id_trip 
	where ssbnr.engineStatus like 'in transit%' and ssbnr.ignition = 'off' and ssm.duration > 200
	
-- canceled  count 2 892
	
create or replace view suivivehicule_statuspos_min_cncl as 
select ssm.id_trip,
1 as id,
ssm.daty_time,
ssm.duration,
ssm.distance,
ssm.is_call_api,
ssm.uid,
ssbnr.speed,
ssbnr.speedMeasure,
ssbnr.odometer,
ssbnr.ignition,
ssbnr.engineTime,
ssbnr.engineStatus
from suivivehicule_statuspos_min ssm
	join suivivehicule_statuspos_bank_notin_record ssbnr on ssm.id_trip = ssbnr.id_trip 
	where ssbnr.engineStatus like 'stopped' or ssbnr.engineStatus like 'idling' and ssbnr.ignition = 'off'  and ssm.duration > 200
	
	
-- idling 777 
	
select ssm.id_trip,
ssm.daty_time,
ssm.duration,
ssm.distance,
ssm.is_call_api,
ssm.uid,
ssbnr.speed,
ssbnr.speedMeasure,
ssbnr.odometer,
ssbnr.ignition,
ssbnr.engineTime,
ssbnr.engineStatus
from suivivehicule_statuspos_min ssm
	join suivivehicule_statuspos_bank_notin_record ssbnr on ssm.id_trip = ssbnr.id_trip 
	where ssbnr.engineStatus like 'idling' and ssbnr.ignition = 'on'  and ssm.duration > 200



update suivivehicule_recordcomment set catno=1 where etat = 1 and comment = ""; 
update suivivehicule_recordcomment set catno=5 where etat = 5 and comment = ""; 
update suivivehicule_recordcomment set catno=11 where etat = 1 and comment = "transit-to-offtrack"; 
