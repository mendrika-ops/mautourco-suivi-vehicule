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
    `spa`.`status` as `status`,
    `spa`.`couleur` as `couleur`,
    `su`.`daty_time` as `datetime`,
    timediff(`stc`.`pick_up_time`, date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s')) as `difftime`,
    `su`.`id` as `idstatusposdetail`,
    `stc`.`trip_start_time` as `trip_start_time`,
    ((time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), `stc`.`trip_start_time`))) * 100) as `pourcentage`,
    `spa`.`id` as `idstatusparameter`
from
    ((`suiviVehicule_trajetcoordonneesummary` `stc`
join `suiviVehicule_statusposdetail` `su` on
    (((`stc`.`id_trip` = `su`.`id_trip`)
        and (`stc`.`Uid` = `su`.`uid`))))
join `suiviVehicule_statusparameter` `spa` on
    (((((time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), `stc`.`trip_start_time`))) * 100) >= `spa`.`min_percent`)
        and (`spa`.`max_percent` > ((time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), date_format(addtime(`su`.`daty_time`, sec_to_time(`su`.`duration`)), '%H:%i:%s'))) / time_to_sec(timediff(addtime(`stc`.`pick_up_time`, '-01:00:00'), `stc`.`trip_start_time`))) * 100)))))
where
    ((`su`.`idmere_id` = (
    select
        max(`ss`.`id`)
    from
        `suiviVehicule_statuspos` `ss`))
    and (str_to_date(`stc`.`trip_start_date`,
    '%m/%d/%Y') = curdate())
        and (`stc`.`pick_up_time` > stc.trip_start_time))
order by
    `spa`.`id`,
    `stc`.`trip_start_date` desc,
    addtime(`stc`.`pick_up_time`, '-01:00:00');

CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `suiviVehicule_laststatuswithorder` AS
 select  `st`.`uid` as `Uid`,
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
    `st`.`PickEnd_H_Pos` as `PickEnd_H_Pos`,
     st.estimatetime  as `estimatetime`,
     st.duration as `duration`,
    `st`.`status` as `status`,
    `st`.`couleur` as `couleur`,
    `st`.`datetime` as `datetime`,
    st.difftime  as `difftime`,
    `st`.`id` as `idstatusposdetail`,
    `st`.`trip_start_time` as `trip_start_time`,
    st.pourcentage as `pourcentage`
	,st.idstatusparameter as  idstatusparameter 
	from suivivehicle_laststatus st where st.status like 'Late' or st.status like 'Risky' ;



create or replace view suiviVehicule_recordtrajet as select 	
 	`svt`.`vehicleno` as `vehicleno`,
    `svt`.`driver_oname` as `driver_oname`,
    `svt`.`FromPlace` as `FromPlace`,
    `svt`.`ToPlace` as `ToPlace`,
    `svt`.`id_trip` as `id_trip`,
    `svt`.`trip_start_date` as `trip_start_date`,
    `svt`.`trip_start_time` as `trip_start_time`,
    `svr`.`comment` as `comment`,
    date_format(`svr`.`datetime`,'%Y-%m-%d') as `daterecord`,
    `svr`.`etat` as `etat`,
    `svr`.`id` as `id`
from suiviVehicule_recordcomment svr join suiviVehicule_trajetcoordonnee svt on svr.id_trip = svt.id_trip ;