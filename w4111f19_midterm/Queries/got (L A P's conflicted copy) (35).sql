CREATE TABLE got_edges_all AS
SELECT Source, Target FROM got-edges
UNION
SELECT Target, Source FROM got-edges

CREATE TABLE one_hop AS
SELECT s.Source AS s_source, t.Target AS 
FROM got_edges_all AS s
JOIN got_edges_all AS t