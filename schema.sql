create database project;

use project;


create table signup
(
id int primary key auto_increment,
name varchar(40),
email varchar(50),
phone bigint(10),
password varchar(40)
);

create table amt
(
accno int primary key,
pin int(4),
amount int
);

create table newacc
(
id int primary key auto_increment,
name varchar(40),
address varchar(100),
phone bigint(11) unique,
accno int unique
);

alter table newacc add constraint fk_amt foreign key(accno) references amt(accno);


create table hist
(
id int primary key auto_increment,
name varchar(40),
histy varchar(100),
datetime datetime
);

select now();

truncate table signup;
truncate table amt;
truncate table newacc;
truncate table hist;


drop table signup;
drop table amt;
drop table newacc;
drop table hist;


select * from signup;
select * from amt;
select * from newacc;
select * from hist;