INSERT INTO repositories (id, github_id, url, name) VALUES
(1, 1, 'testUrl1', 'testName1');

SELECT setval('repositories_id_seq', (SELECT MAX(id) from "repositories"));

INSERT INTO issues (id, github_id, url, title, body, language, repository_id) VALUES
(1, 1, 'testUrl1', 'testTitle1', 'testBody1', 'de', 1);

SELECT setval('issues_id_seq', (SELECT MAX(id) from "issues"));

INSERT INTO commits (id, github_id, url, message, language, issue_id) VALUES
(1, 1, 'testUrl1', 'testMessage1', 'de', 1);

SELECT setval('commits_id_seq', (SELECT MAX(id) from "commits"));

INSERT INTO files (id, sha, url, name, extension, content, patch, commit_id) VALUES
(1, 'testSha1', 'testUrl1', 'testUrl1', 'ext', 'testUrl1', 'testUrl1', 1);

SELECT setval('files_id_seq', (SELECT MAX(id) from "files"));
