CREATE TABLE got_edges_all AS
SELECT Source, Target FROM got-edges
UNION
SELECT Target as Source, Source AS Target FROM got-edges

CREATE TABLE one_hop AS
