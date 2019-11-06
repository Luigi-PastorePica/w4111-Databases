CREATE TABLE got-edges-all AS
SELECT Source, Target FROM got-edges
UNION
SELECT Target as Source, Source AS Target FROM got-edges