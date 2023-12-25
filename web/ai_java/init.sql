CREATE USER 'john'@'%' IDENTIFIED BY 'securepassword';
GRANT ALL PRIVILEGES ON *.* TO 'john'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS ctfjava;
USE ctfjava;
SET NAMES utf8;

DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message` text DEFAULT NULL,
  `username` char(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_ib62m8nph950uc4eiutbqka21` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci;


LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES
(94,'今天我取得了重大突破！经过数月的研究和实验，我成功地发现了人工智能系统中的一个严重漏洞。这个漏洞可能会导致系统在特定条件下产生不可预测的行为，并且可能对系统的安全性和稳定性造成巨大威胁。
我进行了一系列的测试和验证，确保这个漏洞是真实存在的，并且可以在实际应用中被利用。我将尽快与相关机构和公司取得联系，共同解决这个问题，并确保人工智能系统的安全性得到提升
我收到了一些匿名的警告信息。有人似乎对我的研究产生了极大的兴趣，并试图阻止我进一步揭露这个漏洞。这使我感到有些不安，但我决心继续前进，将我的发现公之于众。
我加强了实验室的安全措施，并将我的研究数据备份到多个地方，以防止意外发生。我要确保这个发现不会因为我的离世而彻底消失anM=。

','TvT');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `account_non_expired` bit(1) NOT NULL,
  `account_non_locked` bit(1) NOT NULL,
  `age` int(11) NOT NULL,
  `credentials_non_expired` bit(1) NOT NULL,
  `enabled` bit(1) NOT NULL,
  `password` char(20) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `username` char(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_sb8bbouer5wak8vyiiy4pf2bx` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8 COLLATE utf8_unicode_ci;
INSERT INTO `user` VALUES
    (119, b'1', b'1', 12,b'1',b'1', 'TvT', 'ROLE_user', 'TvT');

