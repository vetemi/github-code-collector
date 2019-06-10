INSERT INTO repositories (id, github_id, url, name) VALUES
(1, 1, 'testUrl1', 'testName1');

SELECT setval('repositories_id_seq', (SELECT MAX(id) from "repositories"));
