create database mautourcosuiviVehicule;

--user
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

--suiviVehicule_trajetcoordonnee
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

--suiviVehicule_units
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


--suiviVehicule_trajetcoordonneesummary
create or replace
algorithm = UNDEFINED view `suiviVehicule_trajetcoordonneesummary` as
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
    (`suiviVehicule_trajetcoordonnee` `st`
join `suiviVehicule_units` `su` on
    ((`st`.`vehicleno` = `su`.`Name`)));    


--suiviVehicule_getlastcoordonnee
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


CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `suivivehicle_laststatus` AS
select
    `su`.`uid` AS `Uid`,
    `stc`.`vehicleno` AS `vehicleno`,
    `stc`.`id` AS `id`,
    `stc`.`driver_oname` AS `driver_oname`,
    `stc`.`driver_mobile_number` AS `driver_mobile_number`,
    `stc`.`FromPlace` AS `FromPlace`,
    `stc`.`ToPlace` AS `ToPlace`,
    `stc`.`id_trip` AS `id_trip`,
    `stc`.`trip_no` AS `trip_no`,
    `stc`.`trip_start_date` AS `trip_start_date`,
    `stc`.`pick_up_time` AS `pick_up_time`,
    `stc`.`PickUp_H_Pos` AS `PickUp_H_Pos`,
    `su`.`coordonnee` AS `PickEnd_H_Pos`,
    addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)) AS `estimatetime`,
    sec_to_time(`su`.`duration`) AS `duration`,
    `spa`.`status` AS `status`,
    `spa`.`couleur` AS `couleur`,
    `su`.`daty_time` AS `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) AS `difftime`,
    `su`.`id` AS `idstatusposdetail`,
    `stc`.`trip_start_time` AS `trip_start_time`,
    ((time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(`stc`.`pick_up_time`, `stc`.`trip_start_time`))) * 100) AS `pourcentage`,
    `spa`.`id` AS `idstatusparameter`,
    `su`.`duration`/60 as difftimestart,
    TIME_TO_SEC(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')))/60 as difftimepickup
from
    ((`suiviVehicule_trajetcoordonneesummary` `stc`
join `suiviVehicule_statusposdetail` `su` on
    (((`stc`.`id_trip` = `su`.`id_trip`)
        and (`stc`.`Uid` = `su`.`uid`))))
join `suiviVehicule_statusparameter` `spa` on
     ((spa.min_percent*60) < time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) and (spa.max_percent*60) > time_to_sec(timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')))))
where
    ((`su`.`idmere_id` = (
    select
        max(`ss`.`id`)
    from
        `suiviVehicule_statuspos` `ss`))
    and (str_to_date(`stc`.`trip_start_date`,
    '%m/%d/%Y') = curdate())
        and (`stc`.`pick_up_time` > `stc`.`trip_start_time`)
            and `stc`.`id_trip` in (
            select
                `svr`.`id_trip`
            from
                `suiviVehicule_recordcomment` `svr` where etat=0) is false)
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


CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `suiviVehicule_recordtrajet` AS
select
    `svt`.`vehicleno` AS `vehicleno`,
    `svt`.`driver_oname` AS `driver_oname`,
    `svt`.`FromPlace` AS `FromPlace`,
    `svt`.`ToPlace` AS `ToPlace`,
    `svt`.`id_trip` AS `id_trip`,
    `svt`.`trip_start_date` AS `trip_start_date`,
    `svt`.`trip_start_time` AS `trip_start_time`,
    `svt`.`pick_up_time` AS `pick_up_time`,
    (case
        when (`svr`.`etat` = 0) then 'Cancel'
        else `svs`.`status`
    end) AS `status`,
    (case
        when (`svr`.`etat` = 0) then 'rgba(30,61,89,1.0)'
        else `svs`.`couleur`
    end) AS `couleur`,
    `svr`.`comment` AS `comment`,
    date_format(`svr`.`datetime`, '%Y-%m-%d') AS `daterecord`,
    `svr`.`etat` AS `etat`,
    `svr`.`id` AS `id`,
    `svt`.`driver_mobile_number` AS `driver_mobile_number`
from
    ((`suiviVehicule_recordcomment` `svr`
join `suiviVehicule_trajetcoordonnee` `svt` on
    ((`svr`.`id_trip` = `svt`.`id_trip`)))
left join `suiviVehicule_statusparameter` `svs` on
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
    end) AS `desce`
from
    `suiviVehicule_statusparameter` `svs`;