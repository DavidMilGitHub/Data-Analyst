CREATE DATABASE SqlProject_DavidMilosheski
GO

USE SqlProject_DavidMilosheski
GO


--Seniority Level 
CREATE TABLE SeniorityLevel (
	ID int IDENTITY(1,1) NOT NULL,
	[Name] NVARCHAR(50) NOT NULL
	CONSTRAINT [PK_SeniorityLevel] PRIMARY KEY CLUSTERED ([ID] ASC)
)
GO

INSERT INTO SeniorityLevel([Name])
VALUES 
	('Junior'),
	('[Intermediate]'),	
	('Senior'),
	('[Lead]'),
	('[Project Manager]'),
	('[Division Manager]'),
	('[Office Manager]'),
	('CEO'),
	('CTO'),
	('CIO')
GO

--Location 
CREATE TABLE [Location] (
	ID int IDENTITY(1,1) NOT NULL,
	CountryName NVARCHAR(100) NULL,
	Continent NVARCHAR(100) NULL,
	Region nvarchar(100) NULL

	CONSTRAINT [PK_Location] PRIMARY KEY CLUSTERED ([ID] ASC)
)
GO

INSERT INTO [Location] 
SELECT
	CountryName,Continent,Region
FROM	
	WideWorldImporters.Application.Countries
GO

--Department 
CREATE TABLE Department (
	ID int IDENTITY(1,1) NOT NULL,
	[Name] NVARCHAR(100) NOT NULL

	CONSTRAINT [PK_Department] PRIMARY KEY CLUSTERED (ID ASC)
)
GO

INSERT INTO Department([Name])
VALUES
	('Personal Banking & Operations'),
	('Digital Banking Department'),
	('Retail Banking & Marketing Department'),
	('Wealth Managment & Third Party Products'),
	('International Banking Division & DFB'),
	('Treasury'),
	('Information Technology'),
	('Corporate Communications'),
	('Support Services & Branch Expansion'),
	('Human Resources')
GO

--Employee
drop table if exists Employee
GO
CREATE TABLE Employee (
	ID int IDENTITY(1,1) NOT NULL,
	FirstName NVARCHAR(100) NOT NULL,
	LastName NVARCHAR(100) NOT NULL,
	[LocationId] int NOT NULL,
	SeniorityLevelId int NOT NULL,
	DepartmentId int NOT NULL

	CONSTRAINT [PK_Employee] PRIMARY KEY CLUSTERED (ID ASC)
)
GO

INSERT INTO Employee(FirstName,LastName,LocationId,SeniorityLevelId,DepartmentId)
SELECT 
	LEFT(FullName, (charindex(' ', FullName) - 1)) as FirstName, 
    RIGHT(FullName, CHARINDEX (' ' ,REVERSE(FullName))-1) as LastName,
	NTILE(222) OVER (ORDER BY PersonId) as LocationId,
	NTILE(10) OVER (ORDER BY PersonId) as SeniorityLevelId,
	NTILE(10) OVER (ORDER BY PersonId) as DepartmentId
FROM
	WideWorldImporters.Application.People
GO

--Salary --Najprvo gi pravime null za da moze da se napolnat tabelite podocna ke gi ALTER-irame i ke gi napravime NOT NULL
CREATE TABLE Salary (
	ID int IDENTITY(1,1) NOT NULL,
	EmployeeId int NULL,
	[Month] smallint NULL,
	[Year] smallint NULL,
	GrossAmount decimal(18,2) NULL,
	NetAmount decimal(18,2) NULL,
	RegularWorkAmount decimal(18,2) NULL,
	BonusAmount decimal(18,2) NULL,
	OvertimeAmount decimal(18,2) NULL,
	VacationDays smallint NULL,
	SickLeaveDays smallint NULL

	CONSTRAINT [PK_Salary] PRIMARY KEY CLUSTERED (ID ASC)
)
GO
--Temp tabeli za Meseci i Godini
drop table if exists #Months
GO
drop table if exists #Years
GO

CREATE TABLE #Months (
	Months smallint
)
GO
INSERT INTO #Months(Months)
VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11),(12)
GO

CREATE TABLE #Years (
	Years smallint
)
GO

DECLARE @cnt INT = '2001'

WHILE @cnt < 2021
BEGIN
	INSERT INTO #Years(Years) VALUES (@cnt)
	SET @cnt = @cnt + 1
END
GO

DROP TABLE IF EXISTS #Temp
CREATE TABLE #Temp (
	years smallint,
	months smallint
)
GO

INSERT INTO #Temp
SELECT Years,Months
FROM #Years
cross join #Months
GO

drop table if exists #T
GO
create table #T (
	i int,
	y int,
	m int
)
GO

insert into #T
select e.ID,t.years,t.months
from dbo.Employee as e
cross join #Temp as t
order by e.ID,t.years,t.months
GO

insert into Salary(EmployeeId,Year,Month)
select t.i,t.y,t.m
from #T as t
order by t.i,t.y,t.m
GO

UPDATE Salary 
SET GrossAmount = 30000 + ABS(CHECKSUM(NewID())) % 30000
GO 

--Update Net Amount
UPDATE Salary
SET NetAmount = GrossAmount * 0.9
GO

--RegularWorkAmount should be 80% of the total Net amount for all employees and months 
UPDATE Salary
SET RegularWorkAmount = NetAmount * 0.8
GO

--Bonus amount should be the difference between the 
---NetAmount and RegularWorkAmount for every Odd month (January,March,..)
UPDATE Salary
SET BonusAmount = NetAmount - RegularWorkAmount
WHERE Month % 2 = 1 
GO

--OvertimeAmount  should be the difference between the 
---NetAmount and RegularWorkAmount for every Even month (February,April,…)
UPDATE Salary
SET OvertimeAmount = NetAmount - RegularWorkAmount
WHERE Month % 2 = 0
GO

---	All employees use 10 vacation days in July and 10 Vacation days in December
UPDATE Salary
SET VacationDays =+ 10
WHERE Month IN (7,12)
GO

---	Additionally random vacation days and sickLeaveDays should be generated with the following script:
update dbo.Salary set VacationDays = VacationDays + (EmployeeId % 2)
where  (EmployeeId + MONTH+ year)%5 = 1
GO
update dbo.Salary set SickLeaveDays = EmployeeId%8, vacationDays = vacationDays + (EmployeeId % 3)
where  (employeeId + MONTH+ year)%5 = 2
GO

--Finalna proverka
select * from dbo.salary 
where NetAmount <> (regularWorkAmount + BonusAmount + OverTimeAmount)

--Gi menuvame NULL vrednostite so 0
update Salary
set BonusAmount = isnull(BonusAmount, 0)
	, OvertimeAmount = isnull(OvertimeAmount, 0)
	, VacationDays = isnull(VacationDays, 0)
	, SickLeaveDays = isnull(SickLeaveDays, 0)


--Alter tables za da nemozeme da vnesemu NULL vrednosti
ALTER TABLE Salary ALTER COLUMN EmployeeID int NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN [Month] smallint NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN [Year] smallint NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN GrossAmount decimal(18,2) NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN NetAmount decimal(18,2) NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN RegularWorkAmount decimal(18,2) NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN BonusAmount decimal(18,2) NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN OvertimeAmount decimal(18,2) NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN VacationDays smallint NOT NULL
GO
ALTER TABLE Salary ALTER COLUMN SickLeaveDays smallint NOT NULL
GO

--Add foreign keys
ALTER TABLE [dbo].Employee  WITH NOCHECK ADD CONSTRAINT [FK_Employee_Location] FOREIGN KEY(LocationId)
REFERENCES [dbo].Location ([Id])
GO

ALTER TABLE [dbo].Employee  WITH NOCHECK ADD CONSTRAINT [FK_Employee_SeniorityLevel] FOREIGN KEY(SeniorityLevelId)
REFERENCES [dbo].SeniorityLevel ([Id])
GO


ALTER TABLE [dbo].Employee  WITH NOCHECK ADD CONSTRAINT [FK_Employee_Department] FOREIGN KEY(DepartmentId)
REFERENCES [dbo].Department ([Id])
GO

ALTER TABLE [dbo].Salary  WITH NOCHECK ADD CONSTRAINT [FK_Salary_Employee] FOREIGN KEY(EmployeeId)
REFERENCES [dbo].Employee ([Id])
GO


