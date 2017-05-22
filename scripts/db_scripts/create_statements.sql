DROP TABLE IF EXISTS tb_player_adv_misc;
DROP TABLE IF EXISTS tb_player_position;
DROP TABLE IF EXISTS tb_player_defense;
DROP TABLE IF EXISTS tb_player_passing;
DROP TABLE IF EXISTS tb_player_rebounding;
DROP TABLE IF EXISTS tb_player_scoring;
DROP TABLE IF EXISTS tb_player_played;
DROP TABLE IF EXISTS tb_player_shot_selection;
DROP TABLE IF EXISTS tb_player_info;
DROP TABLE IF EXISTS tb_player;

CREATE TABLE IF NOT EXISTS tb_player (
  player INTEGER PRIMARY KEY AUTOINCREMENT,
  link VARCHAR(45) NOT NULL,
  name VARCHAR(45) NOT NULL);
  

-- -----------------------------------------------------
-- Table tb_player_info
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_info (
  player_info INTEGER PRIMARY KEY AUTOINCREMENT,
  player INTEGER NOT NULL,
  season VARCHAR(45) NOT NULL,
  age INTEGER NOT NULL,
  team VARCHAR(45) NOT NULL,
  FOREIGN KEY (player) REFERENCES tb_player(player));
  

-- -----------------------------------------------------
-- Table tb_player_shot_selection
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_shot_selection (
  player_shot_selection INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  zero_two_att DECIMAL(4,3) NULL,
  three_nine_att DECIMAL(4,3) NULL,
  ten_fifteen_att DECIMAL(4,3) NULL,
  sixteen_threept_att DECIMAL(4,3) NULL,
  threept_att DECIMAL(4,3) NULL,
  zero_two_made DECIMAL(4,3) NULL,
  three_nine_made DECIMAL(4,3) NULL,
  ten_fifteen_made DECIMAL(4,3) NULL,
  sixteen_threept_made DECIMAL(4,3) NULL,
  threept_att_made DECIMAL(4,3) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_played
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_played (
  player_played INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  games_played INTEGER NULL,
  games_started INTEGER NULL,
  mp INTEGER NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_scoring
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_scoring (
  player_scoring INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  pts_pgm DECIMAL(4,1) NULL,
  ts_ptg DECIMAL(4,3) NULL,
  fg_pg DECIMAL(4,1) NULL,
  fga_pg DECIMAL(4,1) NULL,
  ft_pg DECIMAL(4,1) NULL,
  fta_pg DECIMAL(4,1) NULL,
  ft_per DECIMAL(4,3) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_rebounding
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_rebounding (
  player_rebounding INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  drb_pg DECIMAL(4,1) NULL,
  orb_pg DECIMAL(4,1) NULL,
  drb_per DECIMAL(4,1) NULL,
  orb_per DECIMAL(4,1) NULL,
  trb_per DECIMAL(4,1) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_passing
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_passing (
  player_passing INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  ast_pg DECIMAL(4,1) NULL,
  tov_pg DECIMAL(4,1) NULL,
  ast_per DECIMAL(4,1) NULL,
  tov_per DECIMAL(4,1) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_defense
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_defense (
  player_defense INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  stl_pg DECIMAL(4,1) NULL,
  blk_pg DECIMAL(4,1) NULL,
  pf_pg DECIMAL(4,1) NULL,
  stl_per DECIMAL(4,1) NULL,
  blk_per DECIMAL(4,1) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_position
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_position (
  player_position INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  pg DECIMAL(3,2) NULL,
  sg DECIMAL(3,2) NULL,
  sf DECIMAL(3,2) NULL,
  pf DECIMAL(3,2) NULL,
  c DECIMAL(3,2) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  

-- -----------------------------------------------------
-- Table tb_player_adv_misc
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tb_player_adv_misc (
  player_adv_misc INTEGER PRIMARY KEY AUTOINCREMENT,
  player_info INTEGER NOT NULL,
  ows DECIMAL(4,1) NULL,
  dws DECIMAL(4,1) NULL,
  ws DECIMAL(4,1) NULL,
  wsp48 DECIMAL(4,3) NULL,
  obpm DECIMAL(4,1) NULL,
  dbpm DECIMAL(4,1) NULL,
  bpm DECIMAL(4,1) NULL,
  FOREIGN KEY (player_info)  REFERENCES tb_player_info(player_info));
  
