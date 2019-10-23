DROP TABLE IF EXISTS JOHNS;
DROP VIEW IF EXISTS AverageHeightWeight, AverageHeight;

/*QUESTION 0
EXAMPLE QUESTION
What is the highest salary in baseball history?
*/
Select 1
;
/*SAMPLE ANSWER*/
SELECT MAX(salary) as Max_Salary
FROM Salaries;

/*QUESTION 1
Select the first name, last name, and given name of players who are taller than 6 ft
[hint]: Use "People"
*/
SELECT nameFirst, nameLast, nameGiven
FROM people
WHERE (height/12) > 6;

/*QUESTION 2
Create a Table of all the distinct players with a first name of John who were born in the United States and
played at Fordham university
Include their first name, last name, playerID, and birth state
Add a column called nameFull that is a concatenated version of first and last
[hint] Use a Join between People and CollegePlaying
*/
DROP TABLE IF EXISTS JOHNS;
CREATE Table JOHNS as
SELECT DISTINCT nameFirst, nameLast, concat(nameFirst, ' ', nameLast) AS nameFull, people.playerID, birthState
FROM people
INNER JOIN CollegePlaying
ON people.playerID = CollegePlaying.playerID
WHERE nameFirst='John'AND birthCountry='USA' AND schoolID LIKE 'fordham%';
SELECT * FROM JOHNS; -- For testing purposes

/* The query below gave me the same result as the one above. I pick the one above as my answer for simplicity.*/
-- CREATE Table JOHNS as
-- SELECT DISTINCT nameFirst, nameLast, usJohns.playerID, birthState
-- FROM (SELECT nameFirst, nameLast, playerID, birthState
-- 		FROM people
-- 		WHERE nameFirst='John' AND birthCountry='USA') as usJohns
-- INNER JOIN (SELECT playerID, schoolID 
-- 			FROM CollegePlaying 
--             WHERE schoolID LIKE 'fordham%') as fordhamAlumni
-- ON usJohns.playerID = fordhamAlumni.playerID;
-- SELECT * FROM JOHNS; -- For testing purposes

/*QUESTION 3
Delete all Johns from the above table whose total career runs batted in is less than 2
[hint] use a subquery to select these johns from people by playerid
[hint] you may have to set sql_safe_updates = 1 to delete without a key
*/
SET sql_safe_updates = 0; -- Disable Safe Update Mode because JOHNS has no PK.
DELETE FROM JOHNS
WHERE JOHNS.playerID=(SELECT thejohns.playerID
		FROM (SELECT people.nameFirst, people.nameLast, people.playerID 
				FROM people 
				INNER JOIN JOHNS 
                WHERE people.playerID = JOHNS.playerID) AS thejohns -- This subquery returns all Johns from people that match those in JOHNS.
		INNER JOIN (SELECT sum(RBI) AS total_rbi, playerID 
					FROM Batting 
					GROUP BY playerID) as totalRBI -- This subquery provides total RBI per player in batting.
		ON thejohns.playerID=totalRBI.playerID
		WHERE total_rbi < 2); -- This subquery provides the playerID of all the Johns whose total RBI is less than 2.
SET sql_safe_updates = 1; -- Reenabling Safe Update Mode.
-- SELECT * FROM JOHNS; -- For testing purposes

/*QUESTION 4
Group together players with the same birth year, and report the year, 
 the number of players in the year, and average height for the year
 Order the resulting by year in descending order. Put this in a view
 [hint] height will be NULL for some of these years
*/
-- Temporary answer. Requires more work.
DROP VIEW IF EXISTS AverageHeight;
CREATE VIEW AverageHeight(birthYear, playersBorn, averageHeight)
AS
  SELECT birthYear, count(*) AS players, NULLIF(avg(height), 0) AS averageHeight
  FROM people
  WHERE birthYear IS NOT NULL 
  GROUP BY birthYear
  ORDER BY birthYear DESC;
  -- SELECT * FROM AverageHeight; --  For testing purposes


/*QUESTION 5
Using Question 4, only include groups with an average weight >180 lbs,
also return the average weight of the group. This time, order by ascending
*/
DROP VIEW IF EXISTS AverageHeightWeight;
CREATE VIEW AverageHeightWeight(birthYear, playersBorn, averageHeight, averageWeight)
AS
  SELECT * -- This select wraps around the modified base code from Question 4 in order to discard rows where averageWeight <= 180
  FROM (SELECT birthYear, count(*) AS players, NULLIF(avg(height), 0) as averageHeight, NULLIF(avg(weight), 0) AS averageWeight
		FROM people
		WHERE (birthYear IS NOT NULL)
		GROUP BY birthYear
		ORDER BY birthYear ASC) AS avgHW -- This subquery is the same as Question 4 but including averageWeight
  WHERE avgHW.averageWeight > 180
;
-- SELECT * from AverageHeightWeight; -- For testing purposes

/*QUESTION 6
Find the players who made it into the hall of fame who played for a college located in NY
return the player ID, first name, last name, and school ID. Order the players by School alphabetically.
Update all entries with full name Columbia University to 'Columbia University!' in the schools table
*/
-- Added name_full and state to confirm proper values returned
SELECT people.playerID, nameFirst, nameLast, schoolID, name_full as schoolNameFull, state
FROM people
JOIN (SELECT DISTINCT collegePlaying.schoolID, 
		(IF(schools.name_full LIKE 'Columbia%University%', 'Columbia University!', 
		schools.name_full)) AS name_full, 
        collegePlaying.playerID,  
        schools.state 
	  FROM collegePlaying 
	  INNER JOIN schools
	  ON collegePlaying.schoolID = schools.schoolID AND schools.state = 'NY'
	  ORDER BY collegePlaying.schoolID) AS playedAtNYSchool -- Subquery returns players who played at a NY College and changes Columbia string as required.
ON people.playerID = playedAtNYSchool.playerID; -- Matches player by player ID on both tables

/*QUESTION 7
Find the team id, yearid and average HBP for each team using a subquery.
Limit the total number of entries returned to 100
group the entries by team and year and order by descending values
[hint] be careful to only include entries where AB is > 0
*/
SELECT 1, 1, 1 -- replace with your code
;
