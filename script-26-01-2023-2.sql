
create or replace
algorithm = UNDEFINED view `suiviVehicule_laststatus` as
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
    addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)) as `estimatetime`,
    sec_to_time(`su`.`duration`) as `duration`,
    (case
        when ((time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) <= 60)
        and (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) > 0)) then 'Risky'
        when (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) < 0) then 'Late'
        else 'On time'
    end) as `status`,
    (case
        when ((time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) <= 60)
        and (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) > 0)) then 'rgba(255,192,59,1.0)'
        when (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) < 0) then 'rgba(255,110,64,1.0)'
        else 'rgba(30,132,127,1.0)'
    end) as `couleur`,
    `su`.`daty_time` as `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) as `difftime`
from
    (`suiviVehicule_trajetcoordonneesummary` `stc`
join `suiviVehicule_statusposdetail` `su` on
    ((`stc`.`Uid` = `su`.`uid`)))
where
    ((`su`.`idmere_id` = (
    select
        max(`ss`.`id`)
    from
        `suiviVehicule_statuspos` `ss`))
    and (str_to_date(`stc`.`trip_start_date`,
    '%m/%d/%Y') = curdate())
        and (`stc`.`pick_up_time` >= addtime(curtime(), '-02:00:00')))
order by
    `stc`.`trip_start_date` desc,
    addtime(`stc`.`pick_up_time`, '-01:00:00');


