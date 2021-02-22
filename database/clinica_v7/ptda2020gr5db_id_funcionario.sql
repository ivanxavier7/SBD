CREATE DATABASE  IF NOT EXISTS `clinica` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `clinica`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: clinica
-- ------------------------------------------------------
-- Server version	5.7.17

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
  `funcionario_numero` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `nr_cartao_cidadao` int(11) NOT NULL,
  `nif` bigint(15) NOT NULL,
  `nr_seguranca_social` bigint(11) NOT NULL,
  `data_nascimento` date NOT NULL,
  `telefone` bigint(15) NOT NULL,
  `telemovel` bigint(15) NOT NULL,
  `email` varchar(99) NOT NULL,
  `profissao` varchar(45) NOT NULL,
  `morada` longtext NOT NULL,
  `ativo` tinyint(4) NOT NULL,
  PRIMARY KEY (`funcionario_numero`),
  UNIQUE KEY `nr_cartao_cidadao_UNIQUE` (`nr_cartao_cidadao`),
  UNIQUE KEY `nif_UNIQUE` (`nif`),
  UNIQUE KEY `nr_seguranca_social_UNIQUE` (`nr_seguranca_social`),
  CONSTRAINT `fk_id_funcionario_funcionario1` FOREIGN KEY (`funcionario_numero`) REFERENCES `funcionario` (`numero`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `id_funcionario`
--

LOCK TABLES `id_funcionario` WRITE;
/*!40000 ALTER TABLE `id_funcionario` DISABLE KEYS */;
INSERT INTO `id_funcionario` VALUES (1,'ADMINISTRADOR',0,0,0,'1970-01-01',0,0,'admin@pyclinic','Administrativo','Administrativo',1);
/*!40000 ALTER TABLE `id_funcionario` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`ptda-2020-gr5`@`%`*/ /*!50003 trigger verifica_dados_funcionário before insert on id_funcionario 
	for each row 
	begin 
		if new.data_nascimento >= now() then 
			set new.data_nascimento = null; 
		end if; 
        
        if (length(new.telemovel) > 15 or length(new.telemovel) < 9) then 
			set new.telemovel = null; 
		end if; 
        
        if length(new.nr_cartao_cidadao) != 8 then 
			set new.nr_cartao_cidadao = null; 
		end if; 
        
        if length(new.nr_seguranca_social) != 11 then 
			set new.nr_seguranca_social = null; 
		end if; 
        
        if length(new.nif) != 9 then 
			set new.nif = null; 
		end if; 
        
        if ((length(new.telefone) > 15 or length(new.telefone) < 9)) then 
			set new.telefone = null; 
		end if; 
	end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`ptda-2020-gr5`@`%`*/ /*!50003 trigger verifica_funcionário before update on id_funcionario 
	for each row 
	begin 
		if new.data_nascimento >= now() then 
			set new.data_nascimento = null; 
		end if; 
        
        if (length(new.telemovel) > 15 or length(new.telemovel) < 9) then 
			set new.telemovel = null; 
		end if; 
        
        if length(new.nr_cartao_cidadao) != 8 then 
			set new.nr_cartao_cidadao = null; 
		end if; 
        
        if length(new.nr_seguranca_social) != 11 then 
			set new.nr_seguranca_social = null; 
		end if; 
        
        if length(new.nif) != 9 then 
			set new.nif = null; 
		end if; 
        
        if ((length(new.telefone) > 15 or length(new.telefone) < 9)) then 
			set new.telefone = null; 
		end if; 
	end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-24 20:11:46
