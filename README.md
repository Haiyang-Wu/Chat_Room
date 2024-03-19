# Chat_Room
This is a coursework which is belong to Research Methods and Group Project in Security and Resilience - CSC8208 Group 1
This is database that we used.
```sql
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(64) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `file_size` int NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)


CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message_id` varchar(255) NOT NULL,
  `user_id` varchar(64) NOT NULL,
  `content` text NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'sent',
  PRIMARY KEY (`id`)
)


CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(45) NOT NULL,
  `Password` varchar(128) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `userId_UNIQUE` (`UserID`)
)
