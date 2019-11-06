USE lahman2019clean;

/*batting_summary*/
DROP VIEW IF EXISTS batting_summary;
CREATE VIEW batting_summary AS
	SELECT playerID, yearID, teamID, ROUND(AB, 1) AS AB, ROUND(H, 1) AS H, ROUND(HR, 1) AS HR, ROUND(RBI, 1) AS RBI
    FROM batting;
    
-- Test
SELECT * FROM batting_summary
WHERE playerID='willite01';

/*pitching_summary*/
DROP VIEW IF EXISTS pitching_summary;
CREATE VIEW pitching_summary AS
	SELECT playerID, teamID, yearID, ROUND(W, 1) AS W, ROUND(L, 1) AS L, ROUND(G, 1) AS G_P, ROUND(IPouts, 1) AS IPouts
    FROM pitching;
    
select  playerID, teamID, yearID, W, L, G AS G_P, IPouts from pitching where playerID='willite01';
select  playerID, teamID, yearID, W, L, G AS G_P, IPouts from pitching;

-- Test
select  playerID, teamID, yearID, W, L, G_P, IPouts 
from pitching_summary 
where playerID='willite01';

/*fielding_summary*/
DROP VIEW IF EXISTS fielding_summary;
CREATE VIEW fielding_summary AS
	SELECT playerID, teamID, yearID, SUM(ROUND(PO, 1)) AS PO, SUM(ROUND(A, 1)) AS A, SUM(ROUND(E, 1)) AS E, GROUP_CONCAT(POS)
    FROM fielding
    GROUP BY playerID, teamID, yearID;
    
select playerID, teamID, yearID, PO, A, E, POS from fielding where playerID='willite01';

-- Test
select * from fielding_summary where playerID='willite01';
select playerID, teamID, yearID, PO, A, E, POS from fielding;
SELECT * FROM fielding_summary;

/*appearances_summary*/
DROP VIEW IF EXISTS appearances_summary;
CREATE VIEW appearances_summary AS
	SELECT playerID, teamID, yearID, G_all, GS
    FROM appearances;
    
-- Experiment (realized this is not what the Prof. is asking for).
select * from batting where stint>1;
select playerID, teamID, yearID, G_all, GS from appearances where playerID='abernte02';
select playerID, yearID, SUM(G_all) AS G_all, SUM(GS) AS GS from appearances where playerID='abernte02' GROUP BY playerID, yearID;

-- Test
select * from appearances_summary where playerID='willite01';
select playerID, teamID, yearID, G_all, GS from appearances where playerID='willite01';

/*annual_summary*/
DROP VIEW IF EXISTS annual_summary;
CREATE VIEW annual_summary AS
SELECT * FROM appearances_summary
NATURAL JOIN batting_summary
 JOIN pitching_summary
OUTER JOIN pitching_summary
NATURAL JOIN fielding_summary;


-- Test
SELECT * FROM appearances_summary WHERE playerID='willite01';
SELECT * FROM batting_summary WHERE playerID='willite01';
SELECT * FROM pitching_summary WHERE playerID='willite01';
SELECT * FROM fielding_summary WHERE playerID='willite01';
SELECT * FROM annual_summary WHERE playerID='willite01';
SELECT * FROM annual_summary LIMIT 10;

    
