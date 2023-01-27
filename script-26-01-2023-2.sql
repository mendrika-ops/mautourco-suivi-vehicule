create or replace
view suivivehicle_laststatus as 
select
	`su`.`uid` as `Uid`,
	`stc`.`vehicleno` as `vehicleno`,
	`stc`.`id` as `id`,
	`stc`.`driver_oname` as `driver_oname`,
	`stc`.`driver_mobile_number` as `driver_mobile_number`,
	`stc`.`FromPlace` as `FromPlace`,
	`stc`.`ToPlace` as `ToPlace`,
	`stc`.`id_trip` as `id_trip`,
	`stc`.`trip_no` as `trip_no`,
	`stc`.`trip_start_date` as `trip_start_date`,
	addtime(`stc`.`pick_up_time`, '-01:00:00') as `pick_up_time`,
	`stc`.`PickUp_H_Pos` as `PickUp_H_Pos`,
	`su`.`coordonnee` as `PickEnd_H_Pos`,
	addtime(su.daty_time, sec_to_time(su.duration)) as estimatetime,
	sec_to_time(su.duration) as duration,
	case
		when TIME_TO_SEC(timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s'))) <= 60 and TIME_TO_SEC(timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s'))) > 0 then "Risky"
		when TIME_TO_SEC(timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s'))) < 0 then "Late"
		else "On time"
	end as status,
		case
		when TIME_TO_SEC(timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s'))) <= 60 and TIME_TO_SEC(timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s'))) > 0 then "rgba(255,192,59,1.0)"
		when TIME_TO_SEC(timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s'))) < 0 then "rgba(255,110,64,1.0)"
		else "rgba(30,132,127,1.0)"
	end as couleur,
		su.daty_time as datetime,
		timediff(stc.pick_up_time, DATE_FORMAT(addtime(su.daty_time, sec_to_time(su.duration)), '%H:%i:%s')) as difftime
	from
		(`suivivehicule_trajetcoordonneesummary` `stc`
	join `suivivehicule_statusposdetail` `su` on
		((`stc`.`Uid` = `su`.`uid`)))
	where
		su.idmere_id = (
		select
			max(id)
		from
			suivivehicule_statuspos ss)
		and
	str_to_date(trip_start_date,
		'%m/%d/%Y') = current_date()
		and pick_up_time >= addtime(current_time(), '-02:00:00')
	order by
		trip_start_date desc,
		pick_up_time asc;