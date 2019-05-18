/*!40101 SET character_set_client = utf8 */;

CREATE DATABASE IF NOT EXISTS `codeDB`;

CREATE TABLE IF NOT EXISTS `codeDB`.`repositories` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

  `github_id` INT NOT NULL, 
  `url` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,

  `created` DATETIME NOT NULL DEFAULT NOW(),
  `modified` DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS `codeDB`.`issues` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

  `github_id` INT NOT NULL, 
  `url` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `body_raw` TEXT,
  `body_text_only` TEXT,
  `language` VARCHAR(10),
  `repository_id` INT NOT NULL,

  `created` DATETIME NOT NULL DEFAULT NOW(),
  `modified` DATETIME NOT NULL DEFAULT NOW(),

  CONSTRAINT `fkey_repo_id`
    FOREIGN KEY (`repository_id`) REFERENCES `repositories` (`id`)
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `codeDB`.`commits` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

  `github_id` INT NOT NULL, 
  `url` VARCHAR(255) NOT NULL,
  `body` VARCHAR(255),
  `language` VARCHAR(10),
  `issue_id` INT NOT NULL,

  `created` DATETIME NOT NULL DEFAULT NOW(),
  `modified` DATETIME NOT NULL DEFAULT NOW(),

  CONSTRAINT `fkey_issue_id`
    FOREIGN KEY (`issue_id`) REFERENCES `issues` (`id`)
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `codeDB`.`file` (
  `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

  `sha` VARCHAR(255) NOT NULL, 
  `url` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `ending` VARCHAR(10) NOT NULL,
  `content` TEXT NOT NULL,
  `patch` TEXT NOT NULL,
  `commit_id` INT NOT NULL,

  `created` DATETIME NOT NULL DEFAULT NOW(),
  `modified` DATETIME NOT NULL DEFAULT NOW(),

  CONSTRAINT `fkey_commit_id`
    FOREIGN KEY (`commit_id`) REFERENCES `commits` (`id`)
    ON UPDATE CASCADE
);
