CREATE DATABASE seven;
USE seven;
CREATE TABLE `seven_store`(
    `store_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
    `lat` decimal(16,9) NOT NULL,
    `lng` decimal(16,9) NOT NULL,
    `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
    `address` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
    `lineOA` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
    `tel` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
    `AC` varchar(1) NOT NULL DEFAULT '0',
    `FM` varchar(1) NOT NULL DEFAULT '0',
    `FP` varchar(1) NOT NULL DEFAULT '0',
    `GP` varchar(1) NOT NULL DEFAULT '0',
    `KS` varchar(1) NOT NULL DEFAULT '0',
    `SP` varchar(1) NOT NULL DEFAULT '0',
    `VF` varchar(1) NOT NULL DEFAULT '0',
    `XT` varchar(1) NOT NULL DEFAULT '0',
    PRIMARY KEY (`store_id`),
KEY `seven_store` (`lat`,`lng`)
) CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOAD DATA LOCAL INFILE '{data_file}'
IGNORE INTO TABLE `seven`.`seven_store`
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n' IGNORE 1 ROWS
(store_id, lat, lng, `name`, `address`, lineOA, tel, @AC, @FM, @FP, @GP, @KS, @SP, @VF, @XT)
SET atm=cast(@atm as signed),
AC=cast(@AC as signed),
FM=cast(@FM as signed),
FP=cast(@FP as signed),
GP=cast(@GP as signed),
KS=cast(@KS as signed),
SP=cast(@SP as signed),
VF=cast(@VF as signed),
XT=cast(@v as signed);