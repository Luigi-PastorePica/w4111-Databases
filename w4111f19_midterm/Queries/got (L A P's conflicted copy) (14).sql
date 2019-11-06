CREATE TABLE got_edges_all AS
SELECT Source, Target FROM got-edges
UNION
SELECT Target, Source FROM got-edges

CREATE TABLE one_hop AS
SELECT s.Source AS s_source, s.Target AS s_target, t.Target AS t_Target
FROM got_edges_all AS s
JOIN got_edges_all AS t
ON s.