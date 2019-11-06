use practice_schema;

select * from practice_schema.birth_info;
select * from practice_schema.Astrological_Info;
-- insert into practice_schema.Astrological_Info values ('July', 'Leo');

/*1.*/
select distinct * from Birth_Info 
inner join (select Astrological_Info.astrological_sign from Astrological_Info where Astrological_Info.birth_month < 'September') as reducedAI
where Birth_Info.birth_month='September';

select Astrological_Info.astrological_sign from Astrological_Info where Astrological_Info.birth_month < 'September';
select distinct * from Birth_Info where Birth_Info.birth_month='September';

-- Shouldn't I get something like?
select * from Birth_Info 
inner join (select Astrological_Info.astrological_sign from Astrological_Info where Astrological_Info.birth_month < 'September') as reducedAI
on Birth_Info.birth_month=Astrological_Info.birth_month
where Birth_Info.birth_month='September';

/*2.*/

select distinct Birth_Info.person_name from (Select * from Astrological_Info where Astrological_Info.birth_month='December') as a;

/*3.*/
select distinct * from Birth_Info 
cross join Astrological_Info 
on Birth_Info.birth_month=Astrological_Info.birth_month;

/*4.*/
select distinct Birth_Info.birth_month from Birth_Info
inner join (select Astrological_Info.birth_month from Astrological_Info) as a;

/*5.*/
CREATE TABLE Student(
	UNI Varchar(8) NOT NULL,
	lastName Varchar(15),
	firstName Varchar(15),
	email Varchar(30), 
    PRIMARY KEY (UNI)
    );