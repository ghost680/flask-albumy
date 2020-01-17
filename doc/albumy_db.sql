/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : albumy_db

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2020-01-17 17:41:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for permission
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of permission
-- ----------------------------
INSERT INTO `permission` VALUES ('1', 'FOLLOW');
INSERT INTO `permission` VALUES ('2', 'COLLECT');
INSERT INTO `permission` VALUES ('3', 'COMMENT');
INSERT INTO `permission` VALUES ('4', 'UPLOAD');
INSERT INTO `permission` VALUES ('5', 'MODERATE');
INSERT INTO `permission` VALUES ('6', 'ADMINISTER');

-- ----------------------------
-- Table structure for photo
-- ----------------------------
DROP TABLE IF EXISTS `photo`;
CREATE TABLE `photo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(500) DEFAULT NULL,
  `filename` varchar(64) DEFAULT NULL,
  `filename_s` varchar(64) DEFAULT NULL,
  `filename_m` varchar(64) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of photo
-- ----------------------------
INSERT INTO `photo` VALUES ('1', null, 'ac775018ec6d47a5af050e69a03eb18f.jpg', 'ac775018ec6d47a5af050e69a03eb18f_s.jpg', 'ac775018ec6d47a5af050e69a03eb18f_m.jpg', '2020-01-17 17:35:11', '1');
INSERT INTO `photo` VALUES ('2', null, '4ed1fe6cf7494fb2894a6fd434a1e836.jpg', '4ed1fe6cf7494fb2894a6fd434a1e836_s.jpg', '4ed1fe6cf7494fb2894a6fd434a1e836_m.jpg', '2020-01-17 17:35:15', '1');
INSERT INTO `photo` VALUES ('3', null, '914f9588f1044c1f84b2a3322d7ec009.jpg', '914f9588f1044c1f84b2a3322d7ec009_s.jpg', '914f9588f1044c1f84b2a3322d7ec009_m.jpg', '2020-01-17 17:35:18', '1');
INSERT INTO `photo` VALUES ('4', null, 'c272f09eaba448308ca5c44ce7067a7b.jpg', 'c272f09eaba448308ca5c44ce7067a7b_s.jpg', 'c272f09eaba448308ca5c44ce7067a7b.jpg', '2020-01-17 17:35:24', '1');
INSERT INTO `photo` VALUES ('5', null, 'dd2580d566c64e31831316d8a5d0db2c.jpg', 'dd2580d566c64e31831316d8a5d0db2c_s.jpg', 'dd2580d566c64e31831316d8a5d0db2c_m.jpg', '2020-01-17 17:35:27', '1');
INSERT INTO `photo` VALUES ('6', null, '34884a199e3d4a1aadbe6e810f0971f6.jpg', '34884a199e3d4a1aadbe6e810f0971f6_s.jpg', '34884a199e3d4a1aadbe6e810f0971f6_m.jpg', '2020-01-17 17:36:33', '1');
INSERT INTO `photo` VALUES ('7', null, 'a114fc6113484e5f9c6e0d0539967143.jpg', 'a114fc6113484e5f9c6e0d0539967143_s.jpg', 'a114fc6113484e5f9c6e0d0539967143_m.jpg', '2020-01-17 17:36:54', '1');
INSERT INTO `photo` VALUES ('8', null, '09fcc6a63a0d48ce9a8330085448e093.jpg', '09fcc6a63a0d48ce9a8330085448e093_s.jpg', '09fcc6a63a0d48ce9a8330085448e093.jpg', '2020-01-17 17:37:29', '1');
INSERT INTO `photo` VALUES ('9', null, 'e345aab35843466c99374b186edafaf2.jpg', 'e345aab35843466c99374b186edafaf2_s.jpg', 'e345aab35843466c99374b186edafaf2.jpg', '2020-01-17 17:37:29', '1');
INSERT INTO `photo` VALUES ('10', null, '09091d45c7f544fea2a0a45be8c7ad6b.jpg', '09091d45c7f544fea2a0a45be8c7ad6b_s.jpg', '09091d45c7f544fea2a0a45be8c7ad6b.jpg', '2020-01-17 17:37:29', '1');
INSERT INTO `photo` VALUES ('11', null, 'e1fcb0d9032c40f6add298cd70d66d6e.jpg', 'e1fcb0d9032c40f6add298cd70d66d6e_s.jpg', 'e1fcb0d9032c40f6add298cd70d66d6e.jpg', '2020-01-17 17:37:29', '1');
INSERT INTO `photo` VALUES ('12', null, 'f682cecf98ed48c68f639cca177ad076.jpg', 'f682cecf98ed48c68f639cca177ad076_s.jpg', 'f682cecf98ed48c68f639cca177ad076.jpg', '2020-01-17 17:37:29', '1');
INSERT INTO `photo` VALUES ('13', null, 'fa016d50c8874a80a1e8d7e26cd65acb.jpg', 'fa016d50c8874a80a1e8d7e26cd65acb_s.jpg', 'fa016d50c8874a80a1e8d7e26cd65acb.jpg', '2020-01-17 17:37:29', '1');
INSERT INTO `photo` VALUES ('14', null, '481ddbb93a1343b3a472eb425d1ff39c.jpg', '481ddbb93a1343b3a472eb425d1ff39c_s.jpg', '481ddbb93a1343b3a472eb425d1ff39c_m.jpg', '2020-01-17 17:38:16', '1');
INSERT INTO `photo` VALUES ('15', null, '2c2b13ec11fb43e5a03cf9e8c4e7f7d2.jpg', '2c2b13ec11fb43e5a03cf9e8c4e7f7d2_s.jpg', '2c2b13ec11fb43e5a03cf9e8c4e7f7d2_m.jpg', '2020-01-17 17:38:16', '1');
INSERT INTO `photo` VALUES ('16', null, 'f41ca3e7a3af425bb48af87534f38217.jpg', 'f41ca3e7a3af425bb48af87534f38217_s.jpg', 'f41ca3e7a3af425bb48af87534f38217_m.jpg', '2020-01-17 17:38:16', '1');
INSERT INTO `photo` VALUES ('17', null, '888b1a8b45a2425d968a8b1f62bac530.jpg', '888b1a8b45a2425d968a8b1f62bac530_s.jpg', '888b1a8b45a2425d968a8b1f62bac530_m.jpg', '2020-01-17 17:38:16', '1');
INSERT INTO `photo` VALUES ('18', null, 'fc47e963628e4a66a22734ad6d51bb0c.jpg', 'fc47e963628e4a66a22734ad6d51bb0c_s.jpg', 'fc47e963628e4a66a22734ad6d51bb0c_m.jpg', '2020-01-17 17:38:16', '1');
INSERT INTO `photo` VALUES ('19', null, '596c8c2962214af49c49103cc86c7db7.jpg', '596c8c2962214af49c49103cc86c7db7_s.jpg', '596c8c2962214af49c49103cc86c7db7_m.jpg', '2020-01-17 17:38:16', '1');
INSERT INTO `photo` VALUES ('20', null, '09524b8e31c545559951a2fe05ec674f.jpg', '09524b8e31c545559951a2fe05ec674f_s.jpg', '09524b8e31c545559951a2fe05ec674f_m.jpg', '2020-01-17 17:38:17', '1');
INSERT INTO `photo` VALUES ('21', null, 'b734a7e3addc417fba19314c413624e2.jpg', 'b734a7e3addc417fba19314c413624e2_s.jpg', 'b734a7e3addc417fba19314c413624e2_m.jpg', '2020-01-17 17:38:17', '1');
INSERT INTO `photo` VALUES ('22', null, 'aeca4f7a02764211b66b62efbeaa65e6.jpg', 'aeca4f7a02764211b66b62efbeaa65e6_s.jpg', 'aeca4f7a02764211b66b62efbeaa65e6_m.jpg', '2020-01-17 17:38:17', '1');
INSERT INTO `photo` VALUES ('23', null, 'e197a74cd5c3434380bb2f2705e4d08f.jpg', 'e197a74cd5c3434380bb2f2705e4d08f_s.jpg', 'e197a74cd5c3434380bb2f2705e4d08f.jpg', '2020-01-17 17:38:28', '1');
INSERT INTO `photo` VALUES ('24', null, '6f157f0d6c004ebe9556f423b4290de8.jpg', '6f157f0d6c004ebe9556f423b4290de8_s.jpg', '6f157f0d6c004ebe9556f423b4290de8.jpg', '2020-01-17 17:38:28', '1');
INSERT INTO `photo` VALUES ('25', null, '01cbe8c8cfb34170b2696d164ba1537d.jpg', '01cbe8c8cfb34170b2696d164ba1537d_s.jpg', '01cbe8c8cfb34170b2696d164ba1537d_m.jpg', '2020-01-17 17:38:50', '1');
INSERT INTO `photo` VALUES ('26', null, '2fbf7c65b11f4a10b247f89876ba4aaa.jpg', '2fbf7c65b11f4a10b247f89876ba4aaa_s.jpg', '2fbf7c65b11f4a10b247f89876ba4aaa_m.jpg', '2020-01-17 17:39:10', '1');
INSERT INTO `photo` VALUES ('27', null, '5289cc089efc43f3bc562ce306af1087.jpg', '5289cc089efc43f3bc562ce306af1087_s.jpg', '5289cc089efc43f3bc562ce306af1087.jpg', '2020-01-17 17:39:10', '1');
INSERT INTO `photo` VALUES ('28', null, '79800ffcbdb44df29eaba72483706507.jpg', '79800ffcbdb44df29eaba72483706507_s.jpg', '79800ffcbdb44df29eaba72483706507.jpg', '2020-01-17 17:39:10', '1');
INSERT INTO `photo` VALUES ('29', null, '4a0fc8909ebd4cf99d55409c7eec057d.jpg', '4a0fc8909ebd4cf99d55409c7eec057d_s.jpg', '4a0fc8909ebd4cf99d55409c7eec057d.jpg', '2020-01-17 17:39:11', '1');
INSERT INTO `photo` VALUES ('30', null, '243f68ae992a450ba53de498fc312604.jpg', '243f68ae992a450ba53de498fc312604_s.jpg', '243f68ae992a450ba53de498fc312604_m.jpg', '2020-01-17 17:39:11', '1');
INSERT INTO `photo` VALUES ('31', null, '982bf764e2f347059b302b09877dc3a3.jpg', '982bf764e2f347059b302b09877dc3a3_s.jpg', '982bf764e2f347059b302b09877dc3a3_m.jpg', '2020-01-17 17:39:11', '1');
INSERT INTO `photo` VALUES ('32', null, '0bf2227c6e4547bebc33d92ea5f00d0f.jpg', '0bf2227c6e4547bebc33d92ea5f00d0f_s.jpg', '0bf2227c6e4547bebc33d92ea5f00d0f_m.jpg', '2020-01-17 17:39:11', '1');
INSERT INTO `photo` VALUES ('33', null, '887d34f68e0f4ac182668a8d4ff248b6.jpg', '887d34f68e0f4ac182668a8d4ff248b6_s.jpg', '887d34f68e0f4ac182668a8d4ff248b6_m.jpg', '2020-01-17 17:39:12', '1');
INSERT INTO `photo` VALUES ('34', null, 'a6b05cd3c5de4dbfa8bd0b7d90620f08.jpg', 'a6b05cd3c5de4dbfa8bd0b7d90620f08_s.jpg', 'a6b05cd3c5de4dbfa8bd0b7d90620f08_m.jpg', '2020-01-17 17:39:12', '1');
INSERT INTO `photo` VALUES ('35', null, '7ec82c0de4724f37a19a50110af80699.jpg', '7ec82c0de4724f37a19a50110af80699_s.jpg', '7ec82c0de4724f37a19a50110af80699.jpg', '2020-01-17 17:39:12', '1');
INSERT INTO `photo` VALUES ('36', null, '924630330ef144dea557a9a9de0572e6.jpg', '924630330ef144dea557a9a9de0572e6_s.jpg', '924630330ef144dea557a9a9de0572e6_m.jpg', '2020-01-17 17:39:12', '1');
INSERT INTO `photo` VALUES ('37', null, '0957adbb6d1149ada832372bc5252f98.jpg', '0957adbb6d1149ada832372bc5252f98_s.jpg', '0957adbb6d1149ada832372bc5252f98.jpg', '2020-01-17 17:39:13', '1');
INSERT INTO `photo` VALUES ('38', null, '2d7d40d4ad7f4a58b4103d30671984f8.jpg', '2d7d40d4ad7f4a58b4103d30671984f8_s.jpg', '2d7d40d4ad7f4a58b4103d30671984f8.jpg', '2020-01-17 17:39:13', '1');
INSERT INTO `photo` VALUES ('39', null, '52adf6fd79ea4d4786edaffea155d97d.jpg', '52adf6fd79ea4d4786edaffea155d97d_s.jpg', '52adf6fd79ea4d4786edaffea155d97d.jpg', '2020-01-17 17:39:13', '1');
INSERT INTO `photo` VALUES ('40', null, '994a97186699407eb52ad30b54472932.jpg', '994a97186699407eb52ad30b54472932_s.jpg', '994a97186699407eb52ad30b54472932_m.jpg', '2020-01-17 17:39:13', '1');
INSERT INTO `photo` VALUES ('41', null, '99e26e693b8d47d09890a48bdae7fa91.jpg', '99e26e693b8d47d09890a48bdae7fa91_s.jpg', '99e26e693b8d47d09890a48bdae7fa91_m.jpg', '2020-01-17 17:39:13', '1');
INSERT INTO `photo` VALUES ('42', null, '85309a866930434788baf794a87e24cc.jpg', '85309a866930434788baf794a87e24cc_s.jpg', '85309a866930434788baf794a87e24cc_m.jpg', '2020-01-17 17:39:13', '1');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', 'Locked');
INSERT INTO `role` VALUES ('2', 'User');
INSERT INTO `role` VALUES ('3', 'Moderator');
INSERT INTO `role` VALUES ('4', 'Administrator');

-- ----------------------------
-- Table structure for roles_permissions
-- ----------------------------
DROP TABLE IF EXISTS `roles_permissions`;
CREATE TABLE `roles_permissions` (
  `role_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL,
  KEY `role_id` (`role_id`),
  KEY `permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles_permissions
-- ----------------------------
INSERT INTO `roles_permissions` VALUES ('1', '1');
INSERT INTO `roles_permissions` VALUES ('1', '2');
INSERT INTO `roles_permissions` VALUES ('2', '1');
INSERT INTO `roles_permissions` VALUES ('2', '2');
INSERT INTO `roles_permissions` VALUES ('2', '3');
INSERT INTO `roles_permissions` VALUES ('2', '4');
INSERT INTO `roles_permissions` VALUES ('3', '1');
INSERT INTO `roles_permissions` VALUES ('3', '2');
INSERT INTO `roles_permissions` VALUES ('3', '3');
INSERT INTO `roles_permissions` VALUES ('3', '4');
INSERT INTO `roles_permissions` VALUES ('3', '5');
INSERT INTO `roles_permissions` VALUES ('4', '1');
INSERT INTO `roles_permissions` VALUES ('4', '2');
INSERT INTO `roles_permissions` VALUES ('4', '3');
INSERT INTO `roles_permissions` VALUES ('4', '4');
INSERT INTO `roles_permissions` VALUES ('4', '5');
INSERT INTO `roles_permissions` VALUES ('4', '6');

-- ----------------------------
-- Table structure for taobao
-- ----------------------------
DROP TABLE IF EXISTS `taobao`;
CREATE TABLE `taobao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_links` varchar(120) DEFAULT NULL,
  `book_title` varchar(100) DEFAULT NULL,
  `book_price` varchar(20) DEFAULT NULL,
  `book_isbn` varchar(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_taobao_book_links` (`book_links`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of taobao
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `bio` varchar(120) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `member_since` datetime DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `platform` varchar(20) DEFAULT NULL,
  `browser` varchar(20) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_username` (`username`),
  UNIQUE KEY `ix_user_email` (`email`),
  KEY `role_id` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'ghost', 'ghost2019@qq.com', 'pbkdf2:sha256:150000$PATysxGi$c982e2fd21a08617ee0f6539d00ee1c89966314fa28d2c818daf2796de15e3dc', '钢铁侠', null, null, null, '2020-01-17 17:29:00', '1', '127.0.0.1', 'windows', 'chrome', '79.0.3945.117', '4');
