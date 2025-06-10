-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: access_log
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `entry_log`
--

DROP TABLE IF EXISTS `entry_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entry_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `entry_time` datetime DEFAULT NULL,
  `exit_time` datetime DEFAULT NULL,
  `reason` varchar(200) DEFAULT NULL,
  `plan_number` varchar(50) DEFAULT NULL,
  `sub_reason` varchar(200) DEFAULT NULL,
  `entry_sign` varchar(50) DEFAULT NULL,
  `exit_sign` varchar(50) DEFAULT NULL,
  `witness_name` varchar(50) DEFAULT NULL,
  `witness_team` varchar(100) DEFAULT NULL,
  `witness_sign` varchar(50) DEFAULT NULL,
  `checker_name` varchar(50) DEFAULT NULL,
  `checker_team` varchar(100) DEFAULT NULL,
  `checker_sign` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry_log`
--

LOCK TABLES `entry_log` WRITE;
/*!40000 ALTER TABLE `entry_log` DISABLE KEYS */;
INSERT INTO `entry_log` VALUES (1,'김민수','에이텍','2025-05-30 09:00:00','2025-05-30 12:00:00','서버 점검','WK2025053001','정기점검','김민수','김민수','이수진','IT운영팀','이수진','박정우','보안팀','박정우'),(2,'이영희','비트전자','2025-05-30 10:30:00','2025-05-30 13:00:00','네트워크 교체','WK2025053002','장비설치','이영희','이영희','장우성','네트워크팀','장우성','한지민','보안팀','한지민'),(3,'최준호','디지텍','2025-05-30 08:45:00','2025-05-30 11:30:00','전산 점검','WK2025053003','케이블 정리','최준호','최준호','김소연','시스템팀','김소연','오세훈','보안팀','오세훈'),(4,'박수빈','아이티파크','2025-05-30 09:20:00','2025-05-30 10:50:00','장비 운반','WK2025053004','이동작업','박수빈','박수빈','김형민','시설팀','김형민','정유나','보안팀','정유나'),(5,'강다현','시큐어텍','2025-05-30 13:30:00','2025-05-30 15:00:00','보안 점검','WK2025053005','취약점 확인','강다현','강다현','류지호','보안운영팀','류지호','배지훈','보안팀','배지훈'),(6,'정세영','에이스시스템','2025-05-30 14:00:00','2025-05-30 17:00:00','장비 점검','WK2025053006','기기 이상 확인','정세영','정세영','한유진','운영팀','한유진','송지호','보안팀','송지호'),(7,'이주현','넥스트정보','2025-05-30 11:00:00','2025-05-30 12:30:00','로그 분석','WK2025053007','침해 대응','이주현','이주현','김성우','보안팀','김성우','신유나','보안팀','신유나'),(8,'문지훈','지앤컴퍼니','2025-05-30 09:15:00','2025-05-30 10:30:00','UPS 점검','WK2025053008','정전 대비','문지훈','문지훈','오진아','전력팀','오진아','정윤호','보안팀','정윤호'),(9,'양은지','탑인포','2025-05-30 08:30:00','2025-05-30 09:45:00','장비 반출','WK2025053009','폐기 장비 이동','양은지','양은지','최하늘','운영팀','최하늘','김태경','보안팀','김태경'),(10,'한지훈','메가정보','2025-05-30 16:00:00','2025-05-30 18:00:00','서버 이전','WK2025053010','장비 재배치','한지훈','한지훈','이보람','시스템팀','이보람','윤진호','보안팀','윤진호'),(11,'수기용','테스트 회사','2025-05-30 16:02:45','2025-05-30 16:11:39','테스트를 위해서 출입','WK000445522',NULL,'수기용','수기용','입회자','시스템팀','입회자','김책임','보안팀','김책임'),(12,'김퇴실','삼성전자','2025-05-30 17:53:54',NULL,'전자제품 설치','WR4555445',NULL,'tjaud',NULL,'입회자','IT운영팀','서명','김확인','보안팀','ㅇㅇㅇ'),(13,'메세지','메세지소속회사','2025-05-30 18:00:36',NULL,'메세지전송','WK44dfddfd',NULL,'t아라ㅣㅇ',NULL,'입회자','IT운영팀','서명',NULL,NULL,NULL);
/*!40000 ALTER TABLE `entry_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-09 11:15:13
