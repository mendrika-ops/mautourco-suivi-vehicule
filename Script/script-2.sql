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
    (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / 60) as `difftimepickup`,
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


create or replace
algorithm = UNDEFINED view `suivivehicle_laststatus` as
select
    `ss`.`Uid` as `Uid`,
    `ss`.`vehicleno` as `vehicleno`,
    `ss`.`id` as `id`,
    `ss`.`driver_oname` as `driver_oname`,
    `ss`.`driver_mobile_number` as `driver_mobile_number`,
    `ss`.`FromPlace` as `FromPlace`,
    `ss`.`ToPlace` as `ToPlace`,
    `ss`.`id_trip` as `id_trip`,
    `ss`.`trip_no` as `trip_no`,
    `ss`.`trip_start_date` as `trip_start_date`,
    `ss`.`pick_up_time` as `pick_up_time`,
    `ss`.`PickUp_H_Pos` as `PickUp_H_Pos`,
    `ss`.`PickEnd_H_Pos` as `PickEnd_H_Pos`,
    `ss`.`estimatetime` as `estimatetime`,
    `ss`.`duration` as `duration`,
    (case
        when ((`ss`.`distance` < (
        select
            `sp`.`max_distance`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 5)))
        and (`ss`.`Uid` is not null)) then (
        select
            `sp`.`status`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 5))
        when (`ss`.`difftimestart` <= `ss`.`difftimepickup`) then (
        select
            `sp`.`status`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 4))
        else (
        select
            `sp`.`status`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 1))
    end) as `status`,
    (case
        when ((`ss`.`distance` < (
        select
            `sp`.`max_distance`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 5)))
            and (`ss`.`Uid` is not null)) then (
        select
            `sp`.`couleur`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 5))
        when (`ss`.`difftimestart` <= `ss`.`difftimepickup`) then (
        select
            `sp`.`couleur`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 4))
        else (
        select
            `sp`.`couleur`
        from
            `suivivehicule_statusparameter` `sp`
        where
            (`sp`.`id` = 1))
    end) as `couleur`,
    `ss`.`datetime` as `datetime`,
    `ss`.`difftime` as `difftime`,
    `ss`.`idstatusposdetail` as `idstatusposdetail`,
    `ss`.`trip_start_time` as `trip_start_time`,
    `ss`.`pourcentage` as `pourcentage`,
    (case
        when ((`ss`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5)))
            and (`ss`.`Uid` is not null)) then 5
        when (`ss`.`difftimestart` <= `ss`.`difftimepickup`) then 4
        else 1
    end) as `idstatusparameter`,
    `ss`.`distance` as `distance`,
    `ss`.`difftimestart` as `difftimestart`,
    `ss`.`difftimepickup` as `difftimepickup`,
    `ss`.`current` as `current`
from
    `suivivehicle_laststatus_mere` `ss`;