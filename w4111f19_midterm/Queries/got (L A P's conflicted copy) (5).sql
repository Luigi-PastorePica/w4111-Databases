CREATE TABLE got_edges_all AS
SELECT Source, Target FROM got-edges
UNION
SELECT Target, Source FROM got-edges

CREATE TABLE one_hop AS
SELECT 
