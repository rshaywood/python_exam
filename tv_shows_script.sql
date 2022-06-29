-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tv_shows
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `tv_shows` ;

-- -----------------------------------------------------
-- Schema tv_shows
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tv_shows` DEFAULT CHARACTER SET utf8 ;
USE `tv_shows` ;

-- -----------------------------------------------------
-- Table `tv_shows`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tv_shows`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tv_shows`.`shows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tv_shows`.`shows` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `network` VARCHAR(255) NULL,
  `description` TEXT NULL,
  `release_date` DATE NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tv_shows_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_tv_shows_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `tv_shows`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
