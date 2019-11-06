USE lahman2019clean;

--  Selecting the right group of players based on team, year, and top hitters. 
select batting.playerID, nameLast, teamID, yearID, H from batting, people where teamID='BOS' and yearID=1960 and batting.playerID=people.playerID
order by cast(batting.H as unsigned) desc
limit 10;

-- Two options for obtaining OBP
select playerID, ((H + BB)/(BB + AB)) as OBP from batting;
select playerID, ((cast(H as unsigned) + cast(BB as unsigned))/(cast(BB as unsigned) + cast(AB as unsigned))) as OBP from batting;

-- Obtaining AVG
select playerID, H/AB as AVG from batting;

-- Obtaining SLG
select playerID, teamID, yearID, H, AB, 
(H - 2B - 3B - HR) as 1B, 2B, 3B, HR, 
(((H - 2B - 3B - HR) + 2 * 2B + 3 * 3B + 4 * HR)/AB) as SLG from batting
where teamID='BOS' and yearID=1960
order by SLG Desc;

-- Putting [mostly] everything together
SELECT people.playerID, nameLast, bats, H, AB, 1B, 2B, 3B, HR, RBI, SLG -- , AVG, OBP
from people
natural join (
	select toptenhit.playerID, H, AB, (H - 2B - 3B - HR) as 1B, 2B, 3B, HR, RBI, (((H - 2B - 3B - HR) + 2 * 2B + 3 * 3B + 4 * HR)/AB) as SLG 
    from (select * from batting where teamID='BOS' and yearID='1960' order by CAST(H AS unsigned) DESC limit 10) as toptenhit) as slugging
order by SLG DESC;

-- It seems the professor does not want the top 10 hitters but the top 10 sluggers
SELECT people.playerID, nameLast, bats, H, AB, 1B, 2B, 3B, HR, RBI, ROUND(AVG, 3) AS AVG, ROUND(OBP, 3) AS OBP, ROUND(SLG, 3) AS SLG
FROM people
NATURAL JOIN(
	SELECT batting.playerID, H, AB, (H - 2B - 3B - HR) AS 1B, 2B, 3B, HR, RBI, H/AB AS AVG,
    ((CAST(H AS unsigned) + CAST(BB AS unsigned))/(CAST(BB AS unsigned) + cast(AB AS unsigned))) AS OBP,
    (((H - 2B - 3B - HR) + 2 * 2B + 3 * 3B + 4 * HR)/AB) AS SLG
	FROM batting
    WHERE teamID='BOS' AND yearID=1960
) AS slugging
ORDER BY SLG DESC
LIMIT 10;
