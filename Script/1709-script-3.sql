-- mautourcosuivivehicule.suivivehicle_laststatus_mere source

create or replace
algorithm = UNDEFINED view `suivivehicle_laststatus_mere` as
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
    `stc`.`pick_up_time` as `pick_up_time`,
    `stc`.`PickUp_H_Pos` as `PickUp_H_Pos`,
    `su`.`coordonnee` as `PickEnd_H_Pos`,
    addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)) as `estimatetime`,
    sec_to_time(`su`.`duration`) as `duration`,
    `su`.`daty_time` as `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) as `difftime`,
    `su`.`id` as `idstatusposdetail`,
    `stc`.`trip_start_time` as `trip_start_time`,
    ((time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(`stc`.`pick_up_time`, `stc`.`trip_start_time`))) * 100) as `pourcentage`,
    `su`.`distance` as `distance`,
    (`su`.`duration` / 60) as `difftimestart`,
    (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(`su`.`daty_time`, '%H:%i:%s'))) / 60) as `difftimepickup`,
    `su`.`current` as `current`
from
    (`suivivehicule_trajetcoordonneesummary` `stc`
join `suivivehicule_statusposdetail` `su` on
    ((`stc`.`id_trip` = `su`.`id_trip`)))
where
    ((`su`.`idmere_id` = (
    select
        max(`ss`.`id`)
    from
        `suivivehicule_statuspos` `ss`))
    and (str_to_date(`stc`.`trip_start_date`,
    '%Y-%m-%d') = curdate())
        and `stc`.`id_trip` in (
        select
            `svr`.`id_trip`
        from
            `suivivehicule_recordcomment` `svr`
        where
            (`svr`.`etat` = 0)) is false)
order by
    `stc`.`pick_up_time`;