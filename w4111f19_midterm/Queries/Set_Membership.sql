USE lahman2019clean;
SELECT DISTINCT people.playerID, nameFirst, nameLast
FROM halloffame
INNER JOIN people
	using(playerID)
INNER JOIN appearances
	USING(playerID)
INNER JOIN pitching
	USING(playerID)
INNER JOIN managers
	USING(playerID)
ORDER BY playerID DESC
LIMIT 10;