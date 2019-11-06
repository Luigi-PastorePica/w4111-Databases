USE w4111Midterm;

DROP TABLE IF EXISTS got_edges_all, one_hop, two_hop, three_hop, four_hop;

CREATE TABLE got_edges_all AS
SELECT Source, Target FROM got_edges
UNION
SELECT Target, Source FROM got_edges;

CREATE TABLE one_hop AS
SELECT s.Source AS node0, s.Target AS node1, t.Target AS node_final
FROM got_edges_all AS s
JOIN got_edges_all AS t
ON s.Target = t.Source
WHERE s.Source='Roose' or s.Source='Craster';

CREATE TABLE two_hop AS
SELECT node0, node1, s.node_final as node2, t.Target AS node_final
FROM one_hop AS s
JOIN got_edges_all AS t
ON s.node_final = t.Source
WHERE node0='Roose' or node0='Craster';

CREATE TABLE three_hop AS
SELECT node0, node1, node2, s.node_final AS node3, t.Target AS node_final
FROM two_hop AS s
JOIN got_edges_all AS t
ON s.node_final = t.Source
WHERE node0='Roose' or node0='Craster';

CREATE TABLE four_hop AS
SELECT node0, node1, node2, node3, s.node_final AS node4, t.Target AS node_final
FROM three_hop AS s
JOIN got_edges_all AS t
ON s.node_final = t.Source
WHERE node0='Roose' or node0='Craster';

/* Cool but nope
SELECT * FROM one_hop, two_hop, three_hop, four_hop
WHERE (node0 = 'Roose' and node_final='Craster') or (node0 = 'Craster' and node_final = 'Roose')
LIMIT 20;
*/

SELECT * FROM one_hop
WHERE (node0 = 'Roose' and node_final='Craster') or (node0 = 'Craster' and node_final = 'Roose')
LIMIT 20;

SELECT * FROM two_hop
WHERE (node0 = 'Roose' and node_final='Craster') or (node0 = 'Craster' and node_final = 'Roose')
LIMIT 20;

SELECT * FROM three_hop
WHERE (node0 = 'Roose' and node_final='Craster') or (node0 = 'Craster' and node_final = 'Roose')
LIMIT 20;

SELECT * FROM four_hop
WHERE (node0 = 'Roose' and node_final='Craster') or (node0 = 'Craster' and node_final = 'Roose')
LIMIT 20;