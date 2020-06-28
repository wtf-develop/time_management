# devices
# ------------------------------------------------------------

CREATE TABLE `devices` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL COMMENT 'device owner',
  `name` varchar(80) NOT NULL DEFAULT '' COMMENT 'visible name',
  `state` tinyint(11) DEFAULT 1 COMMENT '0-disabled, 1-enabled',
  `info` varchar(250) DEFAULT '''''',
  `created` bigint(11) NOT NULL DEFAULT 0,
  `lastconnect` bigint(11) DEFAULT 0 COMMENT 'last connection from device',
  `last_ip` varchar(39) DEFAULT '',
  `default` tinyint(4) DEFAULT 0 COMMENT '1-main device for web. Must be created automatically',
  `sync0` tinyint(11) DEFAULT 0 COMMENT 'receive timers values only [-1 or 0]',
  `sync1` tinyint(11) DEFAULT 1 COMMENT 'receive dest day_tasks values only [-1 or 1]',
  `sync2` tinyint(11) DEFAULT 2 COMMENT 'receive dest notes values only [-1 or 2]',
  `sync3` tinyint(11) DEFAULT 3 COMMENT 'receive dest geo values only [-1 or 3]',
  `selected` tinyint(11) DEFAULT 0 COMMENT 'not used now',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_dev_uniq` (`uid`,`name`),
  KEY `ch0_index` (`sync0`),
  KEY `ch1_index` (`sync1`),
  KEY `ch2_index` (`sync2`),
  KEY `ch3_index` (`sync3`),
  KEY `state_index` (`state`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# sync_devices
# ------------------------------------------------------------

CREATE TABLE `sync_devices` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `src` int(11) NOT NULL COMMENT 'source device id',
  `dst` int(11) NOT NULL COMMENT 'destination device id',
  `state` tinyint(11) DEFAULT 1 COMMENT '0-disabled, 1 - enabled',
  `sync0` tinyint(11) DEFAULT -1 COMMENT 'timers values only [-1 or 0]',
  `sync1` tinyint(11) DEFAULT -1 COMMENT 'day_tasks values only [-1 or 1]',
  `sync2` tinyint(11) DEFAULT -1 COMMENT 'notes values only [-1 or 2]',
  `sync3` tinyint(11) DEFAULT -1 COMMENT 'geo values only [-1 or 3]',
  `created` bigint(11) NOT NULL COMMENT 'creation date',
  `invite` varchar(7) DEFAULT NULL COMMENT 'invite from user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `src_dst_uniq` (`src`,`dst`),
  KEY `ch0_index` (`sync0`),
  KEY `ch1_index` (`sync1`),
  KEY `ch2_index` (`sync2`),
  KEY `ch3_index` (`sync3`),
  KEY `dest_index` (`dst`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# sync_tasks
# ------------------------------------------------------------

CREATE TABLE `sync_tasks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `dst` int(11) NOT NULL COMMENT 'id from devices',
  `tid` int(11) NOT NULL COMMENT 'task id',
  `sender` int(11) DEFAULT NULL COMMENT 'sender - only information field. Not indexed',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dst_task_uniq` (`dst`,`tid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# tags
# ------------------------------------------------------------

CREATE TABLE `tags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `created_user` int(11) DEFAULT NULL COMMENT 'only information',
  `created` bigint(20) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_names` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# tasks
# ------------------------------------------------------------

CREATE TABLE `tasks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `globalid` varchar(32) NOT NULL DEFAULT '' COMMENT 'global index generated once (created + "-" random(100000000) + type + repeat_type + hour + minute',
  `devid` int(11) NOT NULL,
  `title` varchar(350) NOT NULL DEFAULT '''''',
  `desc` text NOT NULL,
  `type` tinyint(11) NOT NULL DEFAULT 0 COMMENT '0-timer,1-day plan,2-notes,3-geo',
  `extra` varchar(300) DEFAULT '' COMMENT 'Some extra information in JSON string format',
  `alarm_type` tinyint(11) DEFAULT 0 COMMENT '0-popup,1-signal,2-quite',
  `state` tinyint(11) DEFAULT 20 COMMENT '0-in review, 10-approved, 20-in progress,30- completed, 40- canceled, 50-archived',
  `priority` tinyint(11) DEFAULT 0 COMMENT 'tasks priority (for notes)',
  `locations` varchar(3000) DEFAULT '' COMMENT 'list of locations for this task',
  `start_time` bigint(11) DEFAULT NULL COMMENT 'notify time',
  `done_time` bigint(11) DEFAULT 0 COMMENT 'last done/cancel time',
  `duration_time` mediumint(11) DEFAULT 0 COMMENT 'minutes',
  `update_time` bigint(11) NOT NULL COMMENT 'last change time in ms',
  `update_devid` int(11) DEFAULT NULL COMMENT 'not indexed info, who was last (not used right now)',
  `created` bigint(11) NOT NULL DEFAULT 0 COMMENT 'time when task was created',
  `repeat_type` tinyint(11) DEFAULT 0 COMMENT '0 - without repeat, 1 every day, 2 every week, 3 few days of week, 4 monthly, 5 - quarterly, 6 - annulary',
  `repeat_value` int(11) DEFAULT 0 COMMENT 'repeat_type =2,3: week bit mask. Sunday - bit number 1, 0 bit not used. repeat_type=7, count of days for repeat event',
  `defered_interval` int(11) DEFAULT 0 COMMENT 'task was defered',
  `year` smallint(11) DEFAULT NULL,
  `month` tinyint(11) DEFAULT 1,
  `day` tinyint(11) DEFAULT 1,
  `hour` tinyint(11) DEFAULT 9,
  `minute` tinyint(11) DEFAULT 5,
  `timezone` mediumint(11) DEFAULT 0 COMMENT 'minutes timezone offset',
  `utc_flag` tinyint(11) DEFAULT 0 COMMENT '0-always use local time, 1- use absolute time without timezone',
  `email` varchar(150) DEFAULT '''''',
  `phone` varchar(150) DEFAULT '''''',
  `serial` mediumint(11) NOT NULL COMMENT 'random value up to 10000 after each change',
  PRIMARY KEY (`id`),
  UNIQUE KEY `global_index` (`globalid`),
  KEY `device_index` (`devid`),
  KEY `status of task` (`state`),
  KEY `type_index` (`type`),
  KEY `update_serial_index` (`update_time`,`serial`),
  KEY `start_time_index` (`start_time`),
  KEY `priority_index` (`priority`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# tasks_tags
# ------------------------------------------------------------

CREATE TABLE `tasks_tags` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `taskid` int(11) DEFAULT NULL,
  `tagid` int(11) DEFAULT NULL,
  `created` bigint(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_tag_uniq` (`taskid`,`tagid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;



# users
# ------------------------------------------------------------

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(50) NOT NULL DEFAULT '' COMMENT 'md5 hash',
  `role` varchar(7) DEFAULT '' COMMENT 'not used now',
  `privacy` tinyint(11) DEFAULT 0 COMMENT 'not used now',
  `state` tinyint(4) DEFAULT 1 COMMENT '0-disabled,1-enabled',
  `info` varchar(250) DEFAULT '''''',
  `created` bigint(11) NOT NULL DEFAULT 0,
  `lastlogin` bigint(11) DEFAULT 0 COMMENT 'last loin with web',
  `last_ip` varchar(39) DEFAULT '',
  `fail_login_counter` int(11) DEFAULT 0 COMMENT 'to protect account after few incorrect logins',
  `fail_login_timestamp` bigint(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_login` (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

