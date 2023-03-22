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


CREATE TABLE `suiviVehicule_trajetcoordonnee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicleno` varchar(100) NOT NULL,
  `driver_oname` varchar(150) NOT NULL,
  `driver_mobile_number` varchar(50) NOT NULL,
  `FromPlace` varchar(150) NOT NULL,
  `ToPlace` varchar(150) NOT NULL,
  `id_trip` int NOT NULL,
  `trip_no` int NOT NULL,
  `trip_start_date` varchar(15) NOT NULL,
  `pick_up_time` time(6) NOT NULL,
  `PickUp_H_Pos` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `suiviVehicule_units` (
  `Uid` varchar(50) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `IMEI` varchar(100) DEFAULT NULL,
  `Status` varchar(50) DEFAULT NULL,
  `GroupName` varchar(100) DEFAULT NULL,
  `CompanyName` varchar(100) DEFAULT NULL,
  `PhoneNumber` varchar(100) DEFAULT NULL,
  `UnitType` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
        when (`su`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))) and `su`.`uid` is not null  then (
        select
            `ss`.`status`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))
        else `spa`.`status`
    end) as `status`,
    (case
        when (`su`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))) and `su`.`uid` is not null then (
        select
            `ss`.`couleur`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))
        else `spa`.`couleur`
    end) as `couleur`,
    `su`.`daty_time` as `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) as `difftime`,
    `su`.`id` as `idstatusposdetail`,
    `stc`.`trip_start_time` as `trip_start_time`,
    ((time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(`stc`.`pick_up_time`, `stc`.`trip_start_time`))) * 100) as `pourcentage`,
    (case
        when (`su`.`distance` < (
        select
            `ss`.`max_distance`
        from
            `suivivehicule_statusparameter` `ss`
        where
            (`ss`.`id` = 5))) and `su`.`uid` is not null then 5
        else `spa`.`id`
    end) as `idstatusparameter`,
    `su`.`distance` as `distance`,
    (`su`.`duration` / 60) as `difftimestart`,
    (time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / 60) as `difftimepickup`,
    `su`.`current` as `current`
from
    ((`suivivehicule_trajetcoordonneesummary` `stc`
join `suivivehicule_statusposdetail` `su` on
    (((`stc`.`id_trip` = `su`.`id_trip`))))
join `suivivehicule_statusparameter` `spa` on
    ((((`spa`.`min_percent` * 60) < time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))))
        and ((`spa`.`max_percent` * 60) > time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))))
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
algorithm = UNDEFINED view `suiviVehicule_recordtrajet` as
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
    svr.current,
    date_format(`svr`.`datetime`, ' %H:%i:%s') as actualtime
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


CREATE TABLE `planning` (
  `planning_id` int NOT NULL AUTO_INCREMENT,
  `vehicleno` varchar(100) DEFAULT NULL,
  `driver_oname` varchar(250) DEFAULT NULL,
  `driver_mobile_number` varchar(100) DEFAULT NULL,
  `FromPlace` varchar(250) DEFAULT NULL,
  `ToPlace` varchar(250) DEFAULT NULL,
  `id_trip` int DEFAULT NULL,
  `trip_no` int DEFAULT NULL,
  `trip_start_date` date DEFAULT NULL,
  `pick_up_time` varchar(100) DEFAULT NULL,
  `PickUp_H_Pos` varchar(250) DEFAULT NULL,
  `resa_trans_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`planning_id`)
) ENGINE=InnoDB AUTO_INCREMENT=300 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    