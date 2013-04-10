/* Single line comments are not compatible with Windows line endings */

CREATE DATABASE u413;

USE u413;

CREATE TABLE boards(
	id INT PRIMARY KEY,
	name VARCHAR(32),
	onall BIT,
	hidden BIT
);

/* Create u413's default board list */
INSERT INTO boards(id,name,onall,hidden) VALUES(0,'All',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(1,'Links',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(2,'Site',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(3,'Programmig',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(4,'Anon',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(5,'Video/movies',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(6,'Audio/music',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(7,'Games',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(8,'Literature',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(9,'Math',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(10,'Science/skepticism',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(11,'Foreign',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(12,'Misc',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(13,'Test',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(20,'Brony',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(33,'Religion/spiritualism',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(37,'Comic',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(42,'Life the Universe and Everything',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(69,'NSFW',TRUE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(117,'Halo',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(151,'Anime',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(271,'E',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(314,'Pi',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(403,'Access Denied',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(404,'Error',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(413,'Mod',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(420,'Cannabis',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(511,'Anonymous',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(628,'Tau',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(666,'Hell',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(911,'Emergency',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(1337,'1337',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(2012,'End of the world',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(9001,'OVER NINE THOUSAND',FALSE,FALSE);
INSERT INTO boards(id,name,onall,hidden) VALUES(12345,'Gambling',FALSE,FALSE);

/* Posts begin at 1000 */
CREATE TABLE posts(
	id INT(32) NOT NULL PRIMARY KEY AUTO_INCREMENT,
	topic BIT,
	title VARCHAR(128),
	parent INT,
	owner INT(32),
	editor INT(32),
	post TEXT,
	locked BIT DEFAULT 0,
	edited DATETIME,
	posted DATETIME
);

ALTER TABLE posts AUTO_INCREMENT=1000;

CREATE TABLE sessions(
	id CHAR(64) NOT NULL PRIMARY KEY,
	user INT(32),
	username VARCHAR(32),
	access INT(8),
	expire DATETIME,
	context VARCHAR(32),
	history TEXT,
	cmd VARCHAR(16),
	cmddata TEXT
);

CREATE TABLE users(
	id INT(32) NOT NULL PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(32),
	password CHAR(64),
	access INT(8),
	muted BIT DEFAULT 0,
	alias TEXT
);

CREATE TABLE messages(
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	sender INT(32),
	receiver INT(32),
	seen BIT,
	sent TIMESTAMP,
	topic VARCHAR(128),
	msg TEXT
);

CREATE TABLE wall(
	user INT(32),
	text TEXT,
	posted TIMESTAMP
);

CREATE TABLE nsfwall(
	user INT(32),
	text TEXT,
	posted TIMESTAMP
);
