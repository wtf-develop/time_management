CREATE TABLE `devices` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL COMMENT 'device owner',
  `name` varchar(80) NOT NULL DEFAULT '' COMMENT 'visible name',
  `state` tinyint DEFAULT 1 COMMENT '0-disabled, 1-enabled',
  `info` varchar(250) DEFAULT '''''',
  `created` bigint NOT NULL DEFAULT 0,
  `lastconnect` bigint DEFAULT 0 COMMENT 'last connection from device',
  `last_ip` varchar(39) DEFAULT '',
  `default` tinyint(4) DEFAULT 0 COMMENT '1-main device for web. Must be created automatically',
  `sync0` tinyint DEFAULT 0 COMMENT 'receive timers values only [-1 or 0]',
  `sync1` tinyint DEFAULT 1 COMMENT 'receive dest day_tasks values only [-1 or 1]',
  `sync2` tinyint DEFAULT 2 COMMENT 'receive dest notes values only [-1 or 2]',
  `sync3` tinyint DEFAULT 3 COMMENT 'receive dest geo values only [-1 or 3]',
  `selected` tinyint DEFAULT 0 COMMENT 'not used now',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_dev_uniq` (`uid`,`name`),
  KEY `state_index` (`state`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



CREATE TABLE `sync_devices` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `src` int NOT NULL COMMENT 'source device id',
  `dst` int NOT NULL COMMENT 'destination device id',
  `state` tinyint DEFAULT 1 COMMENT '0-disabled, 1 - enabled',
  `sync0` tinyint DEFAULT -1 COMMENT 'timers values only [-1 or 0]',
  `sync1` tinyint DEFAULT -1 COMMENT 'day_tasks values only [-1 or 1]',
  `sync2` tinyint DEFAULT -1 COMMENT 'notes values only [-1 or 2]',
  `sync3` tinyint DEFAULT -1 COMMENT 'geo values only [-1 or 3]',
  `created` bigint NOT NULL COMMENT 'creation date',
  `invite` varchar(7) DEFAULT NULL COMMENT 'invite from user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `src_dst_uniq` (`src`,`dst`),
  KEY `dest_index` (`dst`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


CREATE TABLE `sync_tags` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `dst` int DEFAULT NULL COMMENT 'to device id',
  `tagid` int DEFAULT NULL COMMENT 'tag to send to device',
  `sender` int DEFAULT NULL COMMENT 'only information field',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `sync_tasks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `dst` int NOT NULL COMMENT 'id from devices',
  `tid` int NOT NULL COMMENT 'task id',
  `sender` int DEFAULT NULL COMMENT 'sender - only information field. Not indexed',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dst_task_uniq` (`dst`,`tid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



CREATE TABLE `tags` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `created_user` int DEFAULT NULL COMMENT 'only information',
  `created` bigint(20) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_names` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



CREATE TABLE `tasks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `globalid` varchar(32) NOT NULL DEFAULT '' COMMENT 'global index generated once (created + "-" random(100000000) + type + repeat_type + hour + minute',
  `devid` int NOT NULL,
  `title` varchar(350) NOT NULL DEFAULT '''''',
  `desc` text NOT NULL,
  `type` tinyint NOT NULL DEFAULT 0 COMMENT '0-timer,1-day plan,2-notes,3-geo',
  `extra` varchar(300) DEFAULT '' COMMENT 'Some extra information in JSON string format',
  `alarm_type` tinyint DEFAULT 0 COMMENT '0-popup,1-signal,2-quite',
  `state` tinyint DEFAULT 20 COMMENT '0-in review, 10-approved, 20-in progress,30- completed, 40- canceled, 50-archived',
  `priority` tinyint DEFAULT 0 COMMENT 'tasks priority (for notes)',
  `locations` varchar(3000) DEFAULT '' COMMENT 'list of locations for this task',
  `start_time` bigint DEFAULT NULL COMMENT 'notify time',
  `done_time` bigint DEFAULT 0 COMMENT 'last done/cancel time',
  `duration_time` mediumint DEFAULT 0 COMMENT 'minutes',
  `update_time` bigint NOT NULL COMMENT 'last change time in ms from device',
  `srv_update_time` bigint DEFAULT 0 COMMENT 'server change update task time (internal clock)',
  `update_devid` int DEFAULT NULL COMMENT 'not indexed info, who was last (not used right now)',
  `created` bigint NOT NULL DEFAULT 0 COMMENT 'time when task was created',
  `repeat_type` tinyint DEFAULT 0 COMMENT '0 - without repeat, 1 every day, 2 every week, 3 few days of week, 4 monthly, 5 - quarterly, 6 - annulary',
  `repeat_value` int DEFAULT 0 COMMENT 'repeat_type =2,3: week bit mask. Sunday - bit number 1, 0 bit not used. repeat_type=7, count of days for repeat event',
  `defered_interval` bigint DEFAULT 0 COMMENT 'task was defered',
  `year` smallint DEFAULT NULL,
  `month` tinyint DEFAULT 1,
  `day` tinyint DEFAULT 1,
  `hour` tinyint DEFAULT 9,
  `minute` tinyint DEFAULT 5,
  `timezone` mediumint DEFAULT 0 COMMENT 'minutes timezone offset',
  `utc_flag` tinyint DEFAULT 0 COMMENT '0-always use local time, 1- use absolute time without timezone',
  `email` varchar(150) DEFAULT '''''',
  `phone` varchar(150) DEFAULT '''''',
  `serial` mediumint NOT NULL COMMENT 'random value up to 10000 after each change',
  PRIMARY KEY (`id`),
  UNIQUE KEY `global_index` (`globalid`),
  KEY `device_index` (`devid`),
  KEY `status of task` (`state`),
  KEY `type_index` (`type`),
  KEY `update_serial_index` (`update_time`,`serial`),
  KEY `start_time_index` (`start_time`),
  KEY `priority_index` (`priority`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



CREATE TABLE `tasks_tags` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `taskid` int DEFAULT NULL,
  `tagid` int DEFAULT NULL,
  `created` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_tag_uniq` (`taskid`,`tagid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(50) NOT NULL DEFAULT '' COMMENT 'md5 hash',
  `role` varchar(7) DEFAULT '' COMMENT 'not used now',
  `privacy` tinyint DEFAULT 0 COMMENT 'not used now',
  `state` tinyint(4) DEFAULT 1 COMMENT '0-disabled,1-enabled',
  `info` varchar(250) DEFAULT '''''',
  `created` bigint NOT NULL DEFAULT 0,
  `lastlogin` bigint DEFAULT 0 COMMENT 'last loin with web',
  `last_ip` varchar(39) DEFAULT '',
  `fail_login_counter` int DEFAULT 0 COMMENT 'to protect account after few incorrect logins',
  `fail_login_timestamp` bigint DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_login` (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
