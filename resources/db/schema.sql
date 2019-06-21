SET client_encoding = 'UTF8';

CREATE TABLE IF NOT EXISTS repositories (
  id SERIAL NOT NULL PRIMARY KEY,

  github_id INT UNIQUE NOT NULL, 
  url VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,

  created TIMESTAMP NOT NULL DEFAULT NOW(),
  modified TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS issues (
  id SERIAL NOT NULL PRIMARY KEY,

  github_id INT UNIQUE NOT NULL, 
  url VARCHAR(255) UNIQUE NOT NULL,
  title VARCHAR(255) NOT NULL,
  body TEXT,
  language VARCHAR(10),
  repository_id INT NOT NULL,

  created TIMESTAMP NOT NULL DEFAULT NOW(),
  modified TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT fkey_repo_id
    FOREIGN KEY (repository_id) REFERENCES repositories (id)
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS commits (
  id SERIAL NOT NULL PRIMARY KEY,

  github_id VARCHAR(255) NOT NULL, 
  url VARCHAR(255) NOT NULL,
  message TEXT,
  language VARCHAR(10),
  issue_id INT NOT NULL,

  created TIMESTAMP NOT NULL DEFAULT NOW(),
  modified TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT fkey_issue_id
    FOREIGN KEY (issue_id) REFERENCES issues (id)
    ON UPDATE CASCADE,

  CONSTRAINT uq_commits 
    UNIQUE(github_id, url)
);

CREATE TABLE IF NOT EXISTS files (
  id SERIAL NOT NULL PRIMARY KEY,

  github_id VARCHAR(255) NOT NULL, 
  url VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  extension VARCHAR(10) NOT NULL,
  content TEXT NOT NULL,
  hash NUMERIC UNIQUE NOT NULL,
  commit_id INT NOT NULL,

  created TIMESTAMP NOT NULL DEFAULT NOW(),
  modified TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT fkey_commit_id
    FOREIGN KEY (commit_id) REFERENCES commits (id)
    ON UPDATE CASCADE,

  CONSTRAINT uq_files_url_github_id 
    UNIQUE(github_id, url),

  CONSTRAINT uq_files_hash_extension 
    UNIQUE(hash, extension)
);

CREATE TABLE IF NOT EXISTS patches (
  id SERIAL NOT NULL PRIMARY KEY,

  content TEXT NOT NULL,
  file_id INT NOT NULL,

  created TIMESTAMP NOT NULL DEFAULT NOW(),
  modified TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT fkey_file_id
    FOREIGN KEY (file_id) REFERENCES files (id)
    ON UPDATE CASCADE
);
