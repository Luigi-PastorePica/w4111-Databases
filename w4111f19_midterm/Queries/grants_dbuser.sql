select * from mysql.user;
show grants for dbuser@localhost;
GRANT DROP ON lahman2019clean.batting_summary TO 'dbuser'@'localhost';
GRANT DROP ON lahman2019clean.appearances_summary TO 'dbuser'@'localhost';
GRANT DROP ON lahman2019clean.pitching_summary TO 'dbuser'@'localhost';
GRANT DROP ON lahman2019clean.annual_summary TO 'dbuser'@'localhost';
GRANT DROP ON lahman2019clean.career_summary TO 'dbuser'@'localhost';

GRANT ALL PRIVILEGES ON collegemodels.* TO 'dbuser'@'localhost';
FLUSH PRIVILEGES;