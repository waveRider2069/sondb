set foreign_key_checks = 1;
set explicit_defaults_for_timestamp = ON;
set autocommit = 1;
#baf
DROP TABLE IF EXISTS users;
CREATE TABLE users(
  idu VARCHAR(18) PRIMARY KEY NOT NULL,
  secret VARCHAR(18) BINARY NOT NULL
)ENGINE = InnoDB
DEFAULT CHARSET =utf8;

# Invitation code
DROP TABLE IF EXISTS codes;
CREATE TABLE codes(
  idc VARCHAR(18) PRIMARY KEY NOT NULL
)ENGINE = InnoDB
DEFAULT CHARSET =utf8;

# subject IDs
DROP TABLE IF EXISTS sub_ids;
CREATE TABLE sub_ids
(
  idu_sub VARCHAR(18)  NOT NULL,
  ids VARCHAR(16) PRIMARY KEY NOT NULL,
  FOREIGN KEY (idu_sub) REFERENCES users (idu) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# Projects
DROP TABLE IF EXISTS projects;
CREATE TABLE projects
(
  idu_proj VARCHAR(18)  NOT NULL,
  idp         VARCHAR(16) PRIMARY KEY NOT NULL,
  title       VARCHAR(64)       NOT NULL,
  abbr        VARCHAR(32)       NOT NULL,
  leader      VARCHAR(32)             NOT NULL,
  start_time  DATE                    NOT NULL,
  dueto_end   DATE                    NOT NULL,
  state       VARCHAR(16)             NOT NULL DEFAULT 'in_progress',
  budget      INT,
  subjectn    INT,
  visits      INT,
  description VARCHAR(500),
  record_time DATETIME                NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME                NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY user_title(idu_proj,title),
  UNIQUE KEY user_abbr(idu_proj,abbr),
  FOREIGN KEY (idu_proj) REFERENCES users (idu) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# Tests
DROP TABLE IF EXISTS tests;
CREATE TABLE tests
(
  idt       VARCHAR(16) PRIMARY KEY NOT NULL,
  test_name VARCHAR(32) UNIQUE      NOT NULL DEFAULT 'others',
  test_desc VARCHAR(64)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


# Records, hearing, personal information
DROP TABLE IF EXISTS sub_records;
CREATE TABLE sub_records
(
  idu_rec VARCHAR(18) NOT NULL,
  idr              VARCHAR(16) NOT NULL,
  ids_rec          VARCHAR(16) NOT NULL,
  record_time      DATETIME DEFAULT CURRENT_TIMESTAMP,
  update_time      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  # personal information
  subname          VARCHAR(16) NOT NULL,
  age_record       INT,
  age              INT,
  phone            VARCHAR(20),
  gender           VARCHAR(8),
  attitude         VARCHAR(16),
  location         VARCHAR(32),
  spare            VARCHAR(16),
  sparenote        VARCHAR(64),
  aidwearing       VARCHAR(16),
  diseases         VARCHAR(128) BINARY,
  comments         VARCHAR(256) BINARY,
  #   Hearing
  air_250r         INT,
  air_500r         INT,
  air_1000r        INT,
  air_2000r        INT,
  air_4000r        INT,
  air_8000r        INT,
  air_avgr         FLOAT,
  air_levelr       VARCHAR(16),

  air_250l         INT,
  air_500l         INT,
  air_1000l        INT,
  air_2000l        INT,
  air_4000l        INT,
  air_8000l        INT,
  air_avgl         FLOAT,
  air_levell       VARCHAR(16),

  bone_250r        INT,
  bone_500r        INT,
  bone_1000r       INT,
  bone_2000r       INT,
  bone_4000r       INT,
  bone_8000r       INT,
  bone_avgr        FLOAT,
  bone_levelr      VARCHAR(16),

  bone_250l        INT,
  bone_500l        INT,
  bone_1000l       INT,
  bone_2000l       INT,
  bone_4000l       INT,
  bone_8000l       INT,
  bone_avgl        FLOAT,
  bone_levell      VARCHAR(16),

  cause_right      VARCHAR(16),
  cause_left       VARCHAR(16),
  shape_right      VARCHAR(16),
  shape_left       VARCHAR(16),
  immittance_right VARCHAR(8),
  immittance_left  VARCHAR(8),
  speech           VARCHAR(16),
  PRIMARY KEY (idr),
  UNIQUE KEY records (ids_rec, record_time),
  FOREIGN KEY (ids_rec) REFERENCES sub_ids (ids) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (idu_rec) REFERENCES users (idu) ON DELETE CASCADE ON UPDATE CASCADE
# FULLTEXT KEY search_comment (comments)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# Project information
DROP TABLE IF EXISTS sub_projects;
CREATE TABLE sub_projects
(
  idr_proj VARCHAR(16) NOT NULL,
  idp_proj VARCHAR(16) NOT NULL,
  isfinish VARCHAR(16) NOT NULL DEFAULT 'no',
  payment  INT         NOT NULL DEFAULT 0,

  UNIQUE KEY (idr_proj, idp_proj),
  FOREIGN KEY (idr_proj) REFERENCES sub_records (idr) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (idp_proj) REFERENCES projects (idp) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


# Test information
DROP TABLE IF EXISTS sub_tests;
CREATE TABLE sub_tests
(
  idr_test VARCHAR(16) NOT NULL,
  idt_test VARCHAR(16) NOT NULL,
  UNIQUE KEY (idr_test, idt_test),
  FOREIGN KEY (idr_test) REFERENCES sub_records (idr) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (idt_test) REFERENCES tests (idt) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# ALTER TABLE sub_records ADD air_125r SMALLINT(6) AFTER comments;
# ALTER TABLE sub_records ADD air_750r SMALLINT(6) AFTER air_500r;
# ALTER TABLE sub_records ADD air_1500r SMALLINT(6) AFTER air_1000r;
# ALTER TABLE sub_records ADD air_3000r SMALLINT(6) AFTER air_2000r;
# ALTER TABLE sub_records ADD air_6000r SMALLINT(6) AFTER air_4000r;
# ALTER TABLE sub_records ADD air_125l SMALLINT(6) AFTER air_levelr;
# ALTER TABLE sub_records ADD air_750l SMALLINT(6) AFTER air_500l;
# ALTER TABLE sub_records ADD air_1500l SMALLINT(6) AFTER air_1000l;
# ALTER TABLE sub_records ADD air_3000l SMALLINT(6) AFTER air_2000l;
# ALTER TABLE sub_records ADD air_6000l SMALLINT(6) AFTER air_4000l;

# ALTER TABLE sub_records ADD bone_125r SMALLINT(6) AFTER air_levell;
# ALTER TABLE sub_records ADD bone_125l SMALLINT(6) AFTER bone_levelr;
# ALTER TABLE sub_records ADD bone_6000r SMALLINT(6) AFTER bone_4000r;
# ALTER TABLE sub_records ADD bone_6000l SMALLINT(6) AFTER bone_4000l;
# ALTER TABLE sub_records ADD bone_750r SMALLINT(6) AFTER bone_500r;
# ALTER TABLE sub_records ADD bone_1500r SMALLINT(6) AFTER bone_1000r;
# ALTER TABLE sub_records ADD bone_3000r SMALLINT(6) AFTER bone_2000r;
# ALTER TABLE sub_records ADD bone_750l SMALLINT(6) AFTER bone_500l;
# ALTER TABLE sub_records ADD bone_1500l SMALLINT(6) AFTER bone_1000l;
# ALTER TABLE sub_records ADD bone_3000l SMALLINT(6) AFTER bone_2000l;




# COMMIT;
# set autocommit =1;

# #####################
#########################
