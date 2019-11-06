CREATE TABLE got_edges_all AS
SELECT Source, Target FROM got-edges
UNION
SELECT Target, Source FROM got-edges

CREATE TABLE one_hop AS
SELECT s.Source AS node0, s.Target AS node1, t.Target AS node2
FROM got_edges_all AS s
JOIN got_edges_all AS t
ON s.Target = t.Source;

CREATE TABLE two_hop AS
SELECT node0, node1, node2, t.Target AS node3
FROM one_hop AS s
JOIN got_edges_all AS t
ON s.node2 = t.Source;

CREATE TABLE three_hop AS
SELECT node0, node1, node2, node3, t.Target AS node4
FROM two_hop AS s
JOIN got_edges_all AS t
ON s.node3 = t.Source;

CREATE TABLE four_hop AS
SELECT node0, node1, node2, node3, node4, t.Target AS node5
FROM three_hop AS s
JOIN got_edges_all AS t
ON s.node4 = t.Source;