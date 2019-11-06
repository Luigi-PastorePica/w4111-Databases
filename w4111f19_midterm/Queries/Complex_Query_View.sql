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
	SELECT playerID, teamID, yearID, ROUND(SUM(W), 1) AS W, ROUND(SUM(L), 1) AS L, ROUND(SUM(G), 1) AS G_P, ROUND(SUM(IPouts), 1) AS IPouts
    FROM pitching
    GROUP BY teamID, yearID;
    
select  playerID, teamID, yearID, W, L, G AS G_P, IPouts from pitching where playerID='willite01';
select  playerID, teamID, yearID, W, L, G AS G_P, IPouts from pitching;
select * from pitching where stint>1;
select * from pitching where playerID='abadfe01' order by yearID;

-- Test
select  playerID, teamID, yearID, W, L, G_P, IPouts 
from pitching_summary 
where playerID='willite01';

/*fielding_summary*/
DROP VIEW IF EXISTS fielding_summary;
CREATE VIEW fielding_summary AS
	SELECT playerID, teamID, yearID, SUM(ROUND(PO, 1)) AS PO, SUM(ROUND(A, 1)) AS A, SUM(ROUND(E, 1)) AS E, GROUP_CONCAT(POS) AS POS
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
NATURAL JOIN (
	SELECT * FROM batting_summary 
    LEFT JOIN pitching_summary 
    USING(playerID, teamID, yearID) 
    UNION 
    SELECT * FROM batting_summary 
    RIGHT JOIN pitching_summary 
    USING(playerID, teamID, yearID)
) AS batting_pitching_summary
NATURAL JOIN fielding_summary;


-- Test
SELECT * FROM appearances_summary WHERE playerID='willite01';
SELECT * FROM batting_summary WHERE playerID='willite01';
SELECT * FROM pitching_summary WHERE playerID='willite01';
SELECT * FROM fielding_summary WHERE playerID='willite01';
SELECT * FROM annual_summary WHERE playerID='willite01';
SELECT * FROM annual_summary LIMIT 10;

select * from fielding where pos is null or pos='' or pos='0' or pos='NA' or pos='na' or pos='N/A' or pos='n/a';
select * from pitching where G is null or G='' or G='0' or G='NA' or G='na' or G='N/A' or G='n/a';
select * from pitching where playerID='willite01';

/*career_summary*/
DROP VIEW IF EXISTS career_summary;
CREATE VIEW career_summary AS
SELECT playerID, SUM(G_all), SUM(GS), SUM(AB), SUM(H), SUM(HR), SUM(RBI), SUM(W), SUM(L), SUM(IPouts), SUM(PO), SUM(A), SUM(E), GROUP_CONCAT(DISTINCT POS) AS POSITIONS 
FROM annual_summary
GROUP BY playerID;

-- THIS SEEMS TO BE IT, THE FINAL VERSION.
DROP VIEW IF EXISTS career_summary;
CREATE VIEW career_summary AS
SELECT annual_summary.playerID, SUM(annual_summary.G_all) AS G_all, SUM(annual_summary.GS) AS GS, -- apearances_summary view
	ROUND(SUM(AB), 0) AS AB, ROUND(SUM(H), 0) AS H, ROUND(SUM(HR), 0) HR, ROUND(SUM(RBI), 0) RBI, -- batting_summary view
    ROUND(SUM(W), 0) AS W, ROUND(SUM(L), 0) AS L, ROUND(SUM(IPouts), 0) AS IPouts, -- pitching_summary view
    ROUND(SUM(annual_summary.PO), 0) AS PO, ROUND(SUM(annual_summary.A), 0) AS A, ROUND(SUM(annual_summary.E), 0) AS E, -- fielding_summary view
    all_fielding_pos.POS AS POSITIONS -- original fielding table
FROM annual_summary
JOIN (
	SELECT playerID, GROUP_CONCAT(DISTINCT POS) AS POS 
	FROM fielding 
    GROUP BY playerID
) AS all_fielding_pos -- This derived table is necessary to avoid duplicate positions in the POSITIONS field.
USING(playerID)
GROUP BY playerID;

-- Test
SELECT * FROM career_summary LIMIT 10;