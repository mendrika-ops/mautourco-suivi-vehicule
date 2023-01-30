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
    `st`.`PickUp_H_Pos` as `PickUp_H_Pos`
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

--suiviVehicule_laststatus
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
    addtime(`stc`.`pick_up_time`, '-01:00:00') as `pick_up_time`,
    `stc`.`PickUp_H_Pos` as `PickUp_H_Pos`,
    `su`.`coordonnee` as `PickEnd_H_Pos`,
    addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)) as `estimatetime`,
    sec_to_time(`su`.`duration`) as `duration`,
     (case
        when ((time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) <= 3600)
        and (time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) > 0)) then 'Risky'
        when (time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) < 0) then 'Late'
        when (time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), addtime(curtime(), '-02:00:00') )) < 0) then 'Terminated'
       
        else 'On time'
    end) as `status`,
    (case
        when ((time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) <= 3600)
        and (time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) > 0)) then 'rgba(255,192,59,1.0)'
        when (time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) < 0) then 'rgba(255,110,64,1.0)'
        when (time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), addtime(curtime(), '-02:00:00') )) < 0) then 'rgba(196,196,196,1.0)'
        else 'rgba(30,132,127,1.0)'
    end) as `couleur`,
    `su`.`daty_time` as `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) as `difftime`
from
    (`suivivehicule_trajetcoordonneesummary` `stc`
join `suivivehicule_statusposdetail` `su` on
    ((`stc`.`Uid` = `su`.`uid`)))
where
    ((`su`.`idmere_id` = (
    select
        max(`ss`.`id`)
    from
        `suivivehicule_statuspos` `ss`))
    and (str_to_date(`stc`.`trip_start_date`,
    '%m/%d/%Y') = curdate())
        and (`stc`.`pick_up_time` >= addtime(curtime(), '-02:00:00')))
order by
    `stc`.`trip_start_date` desc,
    addtime(`stc`.`pick_up_time`, '-01:00:00');