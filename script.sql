create database mautourcosuiviVehicule;

CREATE TABLE user (
	id INT auto_increment NOT NULL,
	username varchar(100) NOT NULL,
	mail varchar(150) NOT NULL,
	pswd varchar(250) NOT NULL,
	description varchar(100) NULL,
	etat INT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_general_ci;

create or replace
algorithm = UNDEFINED view `suiviVehicule_trajetcoordonneemax` as
select
    `st`.`vehicleno` as `vehicleno`,
    `st`.`id` as `id`,
    `st`.`driver_oname` as `driver_oname`,
    `st`.`driver_mobile_number` as `driver_mobile_number`,
    `st`.`FromPlace` as `FromPlace`,
    `st`.`ToPlace` as `ToPlace`,
    `st`.`id_trip` as `id_trip`,
    `st`.`trip_no` as `trip_no`,
    `st`.`trip_start_date` as `trip_start_date`,
    `st`.`pick_up_time` as `pick_up_time`,
    `st`.`PickUp_H_Pos` as `PickUp_H_Pos`,
    `st`.`trip_start_time` as `trip_start_time`,
    `st`.`refresh_id` as `refresh_id`
from
    `suiviVehicule_trajetcoordonnee` `st`
where
    (`st`.`refresh_id` = (
    select
        max(`sr`.`id`)
    from
        `suiviVehicule_refresh` `sr`));

create or replace
algorithm = UNDEFINED view `suivivehicule_trajetcoordonneesummary` as
select
    `su`.`Uid` as `Uid`,
    `st`.`vehicleno` as `vehicleno`,
    `st`.`id` as `id`,
    `st`.`driver_oname` as `driver_oname`,
    `st`.`driver_mobile_number` as `driver_mobile_number`,
    `st`.`FromPlace` as `FromPlace`,
    `st`.`ToPlace` as `ToPlace`,
    `st`.`id_trip` as `id_trip`,
    `st`.`trip_no` as `trip_no`,
    `st`.`trip_start_date` as `trip_start_date`,
    `st`.`pick_up_time` as `pick_up_time`,
    `st`.`PickUp_H_Pos` as `PickUp_H_Pos`,
    `st`.`trip_start_time` as `trip_start_time`
from
    (`suivivehicule_trajetcoordonneemax` `st`
left join `suivivehicule_units` `su` on
    ((`st`.`vehicleno` = `su`.`Name`)));

create or replace
algorithm = UNDEFINED view `suiviVehicule_getlastcoordonnee` as
select
    `su`.`uid` as `uid`,
    `stc`.`vehicleno` as `vehicleno`,
    `su`.`idmere_id` as `idmere_id`,
    `su`.`coordonnee` as `coordonnee`
from
    (`suiviVehicule_trajetcoordonneesummary` `stc`
join `suiviVehicule_statusposdetail` `su` on
    ((`stc`.`Uid` = `su`.`uid`)));

create or replace
algorithm = UNDEFINED view `suivivehicle_laststatus` as
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
    (case
        when ((`su`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5)))
        and (`su`.`uid` is not null)) then (
        select
            `ss`.`status`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))
        when ((`su`.`duration` / 60) <= (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / 60)) then (
        select
            `ss`.`status`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 4))
        else `spa`.`status`
    end) as `status`,
    (case
        when ((`su`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5)))
            and (`su`.`uid` is not null)) then (
        select
            `ss`.`couleur`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))
        when ((`su`.`duration` / 60) <= (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / 60)) then (
        select
            `ss`.`couleur`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 4))
        else `spa`.`couleur`
    end) as `couleur`,
    `su`.`daty_time` as `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) as `difftime`,
    `su`.`id` as `idstatusposdetail`,
    `stc`.`trip_start_time` as `trip_start_time`,
    ((time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(`stc`.`pick_up_time`, `stc`.`trip_start_time`))) * 100) as `pourcentage`,
    (case
        when ((`su`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5)))
            and (`su`.`uid` is not null)) then 5
        when ((`su`.`duration` / 60) <= (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / 60)) then 4
        else `spa`.`id`
    end) as `idstatusparameter`,
    `su`.`distance` as `distance`,
    (`su`.`duration` / 60) as `difftimestart`,
    (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / 60) as `difftimepickup`,
    `su`.`current` as `current`
from
    ((`suivivehicule_trajetcoordonneesummary` `stc`
join `suivivehicule_statusposdetail` `su` on
    ((`stc`.`id_trip` = `su`.`id_trip`)))
join `suivivehicule_statusparameter` `spa` on
    ((((`spa`.`min_percent` * 60) < time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))))
        and ((`spa`.`max_percent` * 60) >= time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))))
            and (`spa`.`desce` >= 1))))
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
    `stc`.`pick_up_time`,
    `spa`.`id`;

CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `suiviVehicule_laststatuswithorder` AS
select
    `st`.`Uid` AS `Uid`,
    `st`.`vehicleno` AS `vehicleno`,
    `st`.`id` AS `id`,
    `st`.`driver_oname` AS `driver_oname`,
    `st`.`driver_mobile_number` AS `driver_mobile_number`,
    `st`.`FromPlace` AS `FromPlace`,
    `st`.`ToPlace` AS `ToPlace`,
    `st`.`id_trip` AS `id_trip`,
    `st`.`trip_no` AS `trip_no`,
    `st`.`trip_start_date` AS `trip_start_date`,
    `st`.`pick_up_time` AS `pick_up_time`,
    `st`.`PickUp_H_Pos` AS `PickUp_H_Pos`,
    `st`.`PickEnd_H_Pos` AS `PickEnd_H_Pos`,
    `st`.`estimatetime` AS `estimatetime`,
    `st`.`duration` AS `duration`,
    `st`.`status` AS `status`,
    `st`.`couleur` AS `couleur`,
    `st`.`datetime` AS `datetime`,
    `st`.`difftime` AS `difftime`,
    `st`.`idstatusposdetail` AS `idstatusposdetail`,
    `st`.`trip_start_time` AS `trip_start_time`,
    `st`.`pourcentage` AS `pourcentage`,
    `st`.`idstatusparameter` AS `idstatusparameter`
	from suivivehicle_laststatus st;


create or replace
algorithm = UNDEFINED view `suivivehicule_recordtrajet` as
select
    `svr`.`vehicleno` as `vehicleno`,
    `svr`.`driver_oname` as `driver_oname`,
    `svr`.`FromPlace` as `FromPlace`,
    `svr`.`ToPlace` as `ToPlace`,
    `svr`.`id_trip` as `id_trip`,
    `svr`.`trip_start_date` as `trip_start_date`,
    `svr`.`pick_up_time` as `pick_up_time`,
    (case
        when (`svr`.`etat` = 0) then 'Cancel'
        else `svs`.`status`
    end) as `status`,
    (case
        when (`svr`.`etat` = 0) then 'rgba(30,61,89,1.0)'
        else `svs`.`couleur`
    end) as `couleur`,
    `svr`.`comment` as `comment`,
    date_format(`svr`.`datetime`, '%Y-%m-%d') as `daterecord`,
    `svr`.`etat` as `etat`,
    `svr`.`id` as `id`,
    `svr`.`driver_mobile_number` as `driver_mobile_number`,
    `svr`.`current` as `current`,
    date_format(`svr`.`datetime`, ' %H:%i:%s') as `actualtime`,
    svr.difftimestart,
    svr.difftimepickup
from
    (`suivivehicule_recordcomment` `svr`
left join `suivivehicule_statusparameter` `svs` on
    ((`svs`.`id` = `svr`.`etat`)));
    


CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `suiviVehicule_statusparameterlib` AS
select
    `svs`.`id` AS `id`,
    `svs`.`status` AS `status`,
    `svs`.`min_percent` AS `min_percent`,
    `svs`.`max_percent` AS `max_percent`,
    `svs`.`couleur` AS `couleur`,
    (case
        when (`svs`.`desce` = 0) then 'Disable'
        else 'Enable'
    end) AS `desce`,
    svs.max_distance 
from
    `suiviVehicule_statusparameter` `svs`;

create or replace
algorithm = UNDEFINED view `suivivehicule_planninglib` as
select
    `st`.`vehicleno` as `vehicleno`,
    `st`.`id` as `id`,
    `st`.`driver_oname` as `driver_oname`,
    `st`.`driver_mobile_number` as `driver_mobile_number`,
    `st`.`FromPlace` as `FromPlace`,
    `st`.`ToPlace` as `ToPlace`,
    `st`.`id_trip` as `id_trip`,
    `st`.`trip_no` as `trip_no`,
    `st`.`trip_start_date` as `trip_start_date`,
    `st`.`pick_up_time` as `pick_up_time`,
    `st`.`PickUp_H_Pos` as `PickUp_H_Pos`,
    `st`.`resa_trans_type` as `resa_trans_type`,
    date_format(`st`.`daty_time`, '%Y-%m-%d') as `daterecord`,
    date_format(`st`.`daty_time`, ' %H:%i:%s') as `actualtime`,
    `st`.`daty_time` as `daty_time`,
    st.gpsid
from
    `suivivehicule_planning` `st`;

create or replace
algorithm = UNDEFINED view `suivivehicule_recordtrajet_export` as
select
    `svr`.`vehicleno` as `vehicleno`,
    `svr`.`driver_oname` as `driver_oname`,
    `svr`.`FromPlace` as `FromPlace`,
    `svr`.`ToPlace` as `ToPlace`,
    `svr`.`id_trip` as `id_trip`,
    `svr`.`trip_start_date` as `trip_start_date`,
    cast(svr.pick_up_time as char) as `pick_up_time`,
    (case
        when (`svr`.`etat` = 0) then 'Cancel'
        else `svs`.`status`
    end) as `status`,
    (case
        when (`svr`.`etat` = 0) then 'rgba(30,61,89,1.0)'
        else `svs`.`couleur`
    end) as `couleur`,
    `svr`.`comment` as `comment`,
    date_format(`svr`.`datetime`, '%Y-%m-%d') as `daterecord`,
    `svr`.`etat` as `etat`,
    `svr`.`id` as `id`,
    `svr`.`driver_mobile_number` as `driver_mobile_number`,
    `svr`.`current` as `current`,
    date_format(`svr`.`datetime`, ' %H:%i:%s') as `actualtime`,
    `svr`.`difftimestart` as `difftimestart`,
    `svr`.`difftimepickup` as `difftimepickup`
from
    (`suivivehicule_recordcomment` `svr`
left join `suivivehicule_statusparameter` `svs` on
    ((`svs`.`id` = `svr`.`etat`)));


create or replace
algorithm = UNDEFINED view `suivivehicule_recaprefresh` as
select
    1 as `id`,
    cast(`ss`.`daty_time` as date) as `date`,
    count(0) as `nbre_call_api`
from
    `suivivehicule_statusposdetail` `ss`
where
    (cast(`ss`.`daty_time` as date) <= '2023-04-27')
group by
    cast(`ss`.`daty_time` as date)
union
select
    1 as `id`,
    cast(`ss`.`daty_time` as date) as `date`,
    count(0) as `nbre_call_api`
from
    `suivivehicule_statusposdetail` `ss`
where
    ((cast(`ss`.`daty_time` as date) > '2023-04-27')
        and (`ss`.`is_call_api` = 1))
group by
    cast(`ss`.`daty_time` as date);