select * from johns; 
#select * from collegeplaying
#where schoolID like 'fordham%';

/*Q2*/
-- DROP TABLE IF EXISTS JOHNS;
-- CREATE Table JOHNS as
-- SELECT DISTINCT nameFirst, nameLast, people.playerID, birthState
-- FROM people
-- INNER JOIN CollegePlaying
-- ON people.playerID = CollegePlaying.playerID
-- WHERE nameFirst='John'AND birthCountry='USA' AND schoolID LIKE 'fordham%';

DROP TABLE IF EXISTS JOHNS;
CREATE Table JOHNS as
SELECT DISTINCT nameFirst, nameLast, usJohns.playerID, birthState, schoolID
FROM (SELECT nameFirst, nameLast, playerID, birthState
		FROM people
		WHERE nameFirst='John' AND birthCountry='USA') as usJohns
INNER JOIN (SELECT playerID, schoolID 
			FROM CollegePlaying 
            WHERE schoolID LIKE 'fordham%') as fordhamAlumni
ON usJohns.playerID = fordhamAlumni.playerID;

/*Q3*/

/*Trying to get to answer for question*/

/*I assume the error thrown by this query is exactly the reason for the hint given in the template*/
-- DELETE FROM JOHNS
-- WHERE playerID IN (SELECT JOHNS.playerID 
-- 		FROM JOHNS
-- 		JOIN(SELECT sum(RBI) as total_rbi, playerID 
-- 				FROM Batting 
-- 				GROUP BY playerID) as totalRBI 
-- 		ON JOHNS.playerID=totalRBI.playerID 
--         WHERE total_rbi < 2); 

SET sql_safe_updates = 0;
DELETE FROM JOHNS
WHERE JOHNS.playerID=(SELECT thejohns.playerID
		FROM (SELECT people.nameFirst, people.nameLast, people.playerID 
				FROM people 
				INNER JOIN JOHNS 
                WHERE people.playerID = JOHNS.playerID) AS thejohns
		INNER JOIN (SELECT sum(RBI) AS total_rbi, playerID 
					FROM Batting 
					GROUP BY playerID) as totalRBI 
		ON thejohns.playerID=totalRBI.playerID
		WHERE total_rbi < 2);
SET sql_safe_updates = 1;
        
/*This is the query that returns the requested John from JOHNS*/        
SELECT thejohns.nameFirst, thejohns.nameLast, thejohns.playerID, totalRBI.total_rbi
FROM (SELECT people.nameFirst, people.nameLast, people.playerID 
		FROM people 
		INNER JOIN JOHNS 
		WHERE people.playerID = JOHNS.playerID) AS thejohns
INNER JOIN (SELECT sum(RBI) AS total_rbi, playerID 
			FROM Batting 
			GROUP BY playerID) as totalRBI 
ON thejohns.playerID=totalRBI.playerID
WHERE total_rbi < 2;

/*Similar to query requested in question, but with people instead of JOHNS*/
SELECT nameFirst, nameLast, people.playerID, totalRBI.total_rbi
FROM people
JOIN (SELECT sum(RBI) as total_rbi, playerID FROM Batting GROUP BY playerID) as totalRBI
ON people.playerID = totalRBI.playerID
WHERE total_rbi < 2;

/*Testig subquery*/
 SELECT sum(RBI) as total_rbi, playerID FROM Batting GROUP BY playerID;
 
/*Q4*/
DROP VIEW IF EXISTS AverageHeight;
CREATE VIEW AverageHeight(birthYear, playersBorn, averageHeight)
AS
  SELECT birthYear, count(*) as players, avg(height) as averageHeight
  FROM people
  WHERE birthYear IS NOT NULL
  GROUP BY birthYear
  ORDER BY birthYear DESC
;
select * from AverageHeight;
select * from AverageHeight where AverageHeight is null;
select playerID, nameFirst, nameLast, height from people where height = '';

/*Final answer given*/
DROP VIEW IF EXISTS AverageHeight;
CREATE VIEW AverageHeight(birthYear, playersBorn, averageHeight)
AS
  SELECT birthYear, count(*) as players, NULLIF(avg(height), 0) as averageHeight
  FROM people
  WHERE birthYear IS NOT NULL 
  GROUP BY birthYear
  ORDER BY birthYear DESC
;
select * from AverageHeight;

/*Q5*/
DROP VIEW IF EXISTS AverageHeightWeight;
CREATE VIEW AverageHeightWeight(birthYear, playersBorn, averageHeight, averageWeight)
AS
  SELECT * FROM (
  SELECT birthYear, count(*) AS players, NULLIF(avg(height), 0) as averageHeight, NULLIF(avg(weight), 0) AS averageWeight
  FROM people
  WHERE (birthYear IS NOT NULL) -- AND (averageWeight > 180)
  GROUP BY birthYear
  ORDER BY birthYear ASC
  ) AS avgHW WHERE avgHW.averageWeight > 180
;
SELECT * from AverageHeightWeight;
select * from schools where state = 'NY';

/*Q6*/

/*Testing a subquery to get playerID of players who studied at a NY school and schoolID of their school*/
SELECT DISTINCT collegePlaying.schoolID, schools.name_full, collegePlaying.playerID,  schools.state 
FROM collegePlaying 
INNER JOIN schools
ON collegePlaying.schoolID = schools.schoolID AND schools.state = 'NY'
ORDER BY collegePlaying.schoolID;

/*Changing the nameFull from Columbia University to Columbia University! Using subquery above*/
-- The UPDATE operation does not work on joint tables, apparently. Below this there is a working statement that does not require an update.
-- UPDATE(SELECT DISTINCT collegePlaying.schoolID, schools.name_full, collegePlaying.playerID,  schools.state 
-- 		FROM collegePlaying 
-- 		INNER JOIN schools
-- 		ON collegePlaying.schoolID = schools.schoolID AND schools.state = 'NY'
-- 		ORDER BY collegePlaying.schoolID) as playedAtNYSchool
-- SET playedAtNYSchool.name_full='Columbia Univeristy!'
-- WHERE playedAtNYSchool.name_full LIKE 'Columbia%University%';

-- This subquery properly changes the string from 'Columbia University' to 'Columbia University! without using an UPDATE'
SELECT DISTINCT collegePlaying.schoolID, (IF(schools.name_full LIKE 'Columbia%University%', 'Columbia University!', 
				schools.name_full)) as name_full, collegePlaying.playerID,  schools.state 
FROM collegePlaying 
INNER JOIN schools
ON collegePlaying.schoolID = schools.schoolID AND schools.state = 'NY'
ORDER BY collegePlaying.schoolID;

/*This version does not provide the changed string 'Columbia University' to 'Columbia University!', nor the full name of the school*/
SELECT people.playerID, nameFirst, nameLast, schoolID
FROM people
JOIN (SELECT DISTINCT collegePlaying.schoolID, collegePlaying.playerID, schools.state 
	FROM collegePlaying 
	INNER JOIN schools
	ON collegePlaying.schoolID = schools.schoolID AND schools.state = 'NY'
	ORDER BY collegePlaying.schoolID) as playedAtNYSchool
ON people.playerID = playedAtNYSchool.playerID;

/*This should be the final version of this answer*/
SELECT people.playerID, nameFirst, nameLast, schoolID, name_full, state
FROM people
JOIN (SELECT DISTINCT collegePlaying.schoolID, 
		(IF(schools.name_full LIKE 'Columbia%University%', 'Columbia University!', 
		schools.name_full)) AS name_full, 
        collegePlaying.playerID,  
        schools.state 
	  FROM collegePlaying 
	  INNER JOIN schools
	  ON collegePlaying.schoolID = schools.schoolID AND schools.state = 'NY'
	  ORDER BY collegePlaying.schoolID) as playedAtNYSchool
ON people.playerID = playedAtNYSchool.playerID;

/*Q7*/

/*Most basic version. Returns required fields but does not take into account AB, nor limits returned values*/
SELECT teamID, yearID, avg(HBP) as averageHBP
FROM teams
GROUP BY teamID, yearID
ORDER BY averageHBP DESC
;

SELECT teamID, yearID, avg(HBP) as averageHBP
FROM teams
WHERE AB !=0
GROUP BY teamID, yearID
ORDER BY averageHBP DESC
;

SELECT teamID, yearID, avg(HBP) as averageHBP
FROM batting
WHERE AB !=0
GROUP BY teamID, yearID
ORDER BY averageHBP DESC
LIMIT 100
;

SELECT teamID, yearID, AB, HBP 
FROM teams
Where AB = 0;

SELECT playerID, teamID, yearID, AB, HBP 
FROM batting
Where AB = 0;