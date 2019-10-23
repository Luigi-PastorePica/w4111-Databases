use practice_schema;

# 5.a
SELECT name, birth_month, astrological_sign 
FROM birth_info 
Left JOIN astrological_info 
ON birth_info.birth_month = astrological_info.month;

# 5.b
(SELECT name, birth_month, astrological_sign 
FROM birth_info 
Left JOIN astrological_info 
ON birth_info.birth_month = astrological_info.month)
union
(select name, birth_month, astrological_sign
from birth_info
RIGHT JOIN astrological_info
ON birth_info.birth_month = astrological_info.month);

# 5.c
SELECT name, birth_month, astrological_sign 
FROM birth_info 
INNER JOIN astrological_info 
ON birth_info.birth_month = astrological_info.month; 

# 5.d
SELECT name, birth_month, astrological_sign 
FROM birth_info 
RIGHT JOIN astrological_info 
ON birth_info.birth_month = astrological_info.month;