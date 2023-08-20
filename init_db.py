import mysql.connector
from mysql.connector import errorcode

databases = "WadFinalWebsite"
charset = "utf8"
conn = mysql.connector.connect(host="127.0.0.1", port=3306,
                               user="root", password="zhuxiaoyao99",
                               database="sys", charset=charset,
                               buffered=True,
                               )
cursor = conn.cursor(dictionary=True)

def init_db():
    sql_list = [
        """CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `user_passworld` varchar(255) NOT NULL,
  `user_account` enum('common','admin') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'common',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8""",
        """CREATE TABLE `topic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8""",
        """CREATE TABLE `claim` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8""",
        """CREATE TABLE `claim_relation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `claim_id_1` int DEFAULT NULL,
  `claim_id_2` int DEFAULT NULL,
  `type` enum('opposed','equivalent') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT 'opposed',
  PRIMARY KEY (`id`),
  KEY `claim_id_1` (`claim_id_1`),
  KEY `claim_id_2` (`claim_id_2`),
  CONSTRAINT `claim_id_1` FOREIGN KEY (`claim_id_1`) REFERENCES `claim` (`id`),
  CONSTRAINT `claim_id_2` FOREIGN KEY (`claim_id_2`) REFERENCES `claim` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8""",
        """CREATE TABLE `reply` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8""",
    ]
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {databases} DEFAULT CHARSET '{charset}'")
    except Exception as e:
        pass

    cursor.execute('USE {}'.format(databases))

    for table_sql in sql_list:
        try:
            cursor.execute(table_sql)
        except Exception as e:
            pass
init_db()