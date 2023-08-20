-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: wadfinalwebsite
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `claim`
--

DROP TABLE IF EXISTS `claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim` (
  `id` int NOT NULL AUTO_INCREMENT,
  `heading` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `topic_id` int DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_key` (`user_id`),
  KEY `topic_id_key` (`topic_id`),
  CONSTRAINT `topic_id_key` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`),
  CONSTRAINT `user_id_key` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `claim`
--

LOCK TABLES `claim` WRITE;
/*!40000 ALTER TABLE `claim` DISABLE KEYS */;
INSERT INTO `claim` VALUES (1,'User can enter easily',1,1,'2021-12-14 19:34:29'),(2,'User can not do that!',1,1,'2021-12-14 19:35:45'),(10,'User\'s right',1,1,'2021-12-22 13:39:30'),(11,'XXX',2,1,'2021-12-22 15:11:20'),(12,'ZAD',2,1,'2021-12-22 15:45:06'),(13,'QT',2,2,'2021-12-22 15:46:46'),(14,'ZNHY',2,2,'2021-12-22 15:47:22'),(15,'ZWHY',2,3,'2021-12-22 15:47:38'),(16,'ZZZ',2,1,'2021-12-22 16:09:10'),(17,'WWWW',2,1,'2021-12-22 16:39:22'),(18,'QOP',2,1,'2021-12-22 16:49:51'),(19,'ZAZ',2,1,'2021-12-22 16:51:04'),(20,'QERTXZ',2,1,'2021-12-22 17:14:48'),(21,'2022 is great!',5,8,'2022-01-02 00:42:11'),(22,'2022 was nothing serious',5,8,'2022-01-02 00:44:43');
/*!40000 ALTER TABLE `claim` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `claim_relation`
--

DROP TABLE IF EXISTS `claim_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `claim_relation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `claim_id_1` int DEFAULT NULL,
  `claim_id_2` int DEFAULT NULL,
  `type` enum('opposed','equivalent') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'opposed',
  PRIMARY KEY (`id`),
  KEY `claim_id_1` (`claim_id_1`),
  KEY `claim_id_2` (`claim_id_2`),
  CONSTRAINT `claim_id_1` FOREIGN KEY (`claim_id_1`) REFERENCES `claim` (`id`),
  CONSTRAINT `claim_id_2` FOREIGN KEY (`claim_id_2`) REFERENCES `claim` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `claim_relation`
--

LOCK TABLES `claim_relation` WRITE;
/*!40000 ALTER TABLE `claim_relation` DISABLE KEYS */;
INSERT INTO `claim_relation` VALUES (1,2,1,'opposed'),(2,10,1,'opposed'),(3,10,2,'equivalent'),(4,12,1,'opposed'),(5,12,2,'opposed'),(6,12,10,'opposed'),(7,12,11,'opposed'),(8,14,1,'opposed'),(9,18,1,'opposed'),(10,18,2,'equivalent'),(11,19,1,'opposed'),(12,19,2,'equivalent'),(13,20,1,'opposed'),(14,20,2,'opposed'),(15,20,11,'opposed'),(16,21,11,'equivalent'),(17,22,11,'opposed'),(18,22,21,'equivalent');
/*!40000 ALTER TABLE `claim_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` datetime DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `claim_id` int DEFAULT NULL,
  `reply_id` int DEFAULT NULL,
  `claim` enum('','clarification','supporting argument','counterargument') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `reply` enum('','evidence','support','rebuttal') DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `user_id_key2` (`user_id`),
  KEY `claim_id_key` (`claim_id`),
  KEY `reply_id_key` (`reply_id`),
  CONSTRAINT `claim_id_key` FOREIGN KEY (`claim_id`) REFERENCES `claim` (`id`),
  CONSTRAINT `reply_id_key` FOREIGN KEY (`reply_id`) REFERENCES `reply` (`id`),
  CONSTRAINT `user_id_key2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
INSERT INTO `reply` VALUES (4,'2021-12-22 13:40:19','absolutely',1,10,NULL,'clarification',''),(5,'2021-12-22 13:40:33','OK',1,10,4,'','support'),(6,'2021-12-22 14:28:31','？',1,1,5,'','evidence'),(7,'2021-12-22 14:28:36','。?',1,1,6,'','evidence'),(8,'2021-12-22 14:28:40','??',1,1,7,'','evidence'),(9,'2021-12-22 14:28:44','？',1,1,8,'','evidence'),(10,'2021-12-22 14:28:49','？？',1,1,9,'','evidence'),(11,'2021-12-22 14:28:58','？/??',1,1,10,'','evidence'),(12,'2021-12-22 14:29:06',',,',1,1,6,'','evidence'),(13,'2021-12-22 15:46:03','WTF',2,12,NULL,'clarification',''),(14,'2021-12-22 16:46:38','ww',2,17,NULL,'clarification',''),(15,'2021-12-22 16:46:51','6346346',2,17,NULL,'clarification',''),(16,'2021-12-22 16:47:59','QQQ',2,1,NULL,'clarification',''),(17,'2021-12-22 16:48:07','AAA',2,1,16,'','evidence'),(18,'2021-12-31 00:26:50','QWER',1,1,17,'','evidence'),(19,'2022-01-02 00:42:36','I\'m totally agree with u!',5,21,NULL,'clarification',''),(20,'2022-01-02 00:43:03','I agree with u too',5,21,19,'','support'),(21,'2022-01-02 00:43:31','I will be a better man!',5,21,NULL,'counterargument',''),(22,'2022-01-02 00:43:55','believe urself！',5,21,21,'','rebuttal'),(23,'2022-01-02 00:45:59','flat year',5,22,NULL,'supporting argument',''),(24,'2022-01-02 00:46:15','It should be wonderful！',5,22,23,'','rebuttal');
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (1,'User can enter whatever they want',1,'2021-12-14 19:33:49'),(2,'Sean',1,'2021-12-22 13:39:05'),(3,'shit',1,'2021-12-22 14:18:10'),(4,'QQ',2,'2021-12-22 15:31:58'),(5,'QT',2,'2021-12-22 15:32:13'),(6,'Sean',3,'2021-12-31 01:23:42'),(7,'Testing is funny,init?',4,'2021-12-31 03:03:42'),(8,'Wonderful 2022!',5,'2022-01-02 00:41:37');
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `user_passworld` varchar(255) NOT NULL,
  `user_account` enum('common','admin') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'common',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Sean','fdb0c2ac94d4239a235373ddd080e02d','common'),(2,'Zhu','fdb0c2ac94d4239a235373ddd080e02d','common'),(3,'XXX','fdb0c2ac94d4239a235373ddd080e02d','common'),(4,'CleverBoy','202cb962ac59075b964b07152d234b70','common'),(5,'HappyNewYear','dab89a7861858b1f51b5e9f1df939e10','common');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-02  1:25:22
