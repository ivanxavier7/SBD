CREATE DATABASE  IF NOT EXISTS `clinica` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `clinica`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: clinica
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `id_funcionario`
--

DROP TABLE IF EXISTS `id_funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `id_funcionario` (
  `funcionario_numero` int NOT NULL,
  `nome` varchar(255) NOT NULL,
  `nr_cartao_cidadao` int NOT NULL,
  `nif` int NOT NULL,
  `nr_seguranca_social` int NOT NULL,
  `data_nascimento` date NOT NULL,
  `telefone` int NOT NULL,
  `telemovel` int NOT NULL,
  `email` varchar(99) NOT NULL,
  `morada` longtext NOT NULL,
  `profissao` varchar(45) NOT NULL,
  `ativo` tinyint NOT NULL,
  PRIMARY KEY (`funcionario_numero`),
  CONSTRAINT `fk_id_funcionario_funcionario1` FOREIGN KEY (`funcionario_numero`) REFERENCES `funcionario` (`numero`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `id_funcionario`
--

LOCK TABLES `id_funcionario` WRITE;
/*!40000 ALTER TABLE `id_funcionario` DISABLE KEYS */;
INSERT INTO `id_funcionario` VALUES (1,'ADMINISTRADOR',0,0,0,'1970-01-01',0,0,'admin@pyclinic','PyClinic','Administrativo',1);
/*!40000 ALTER TABLE `id_funcionario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-21  2:51:14
