USE employees;
SHOW TABLES;
DESCRIBE employees;
-- #5 different data types: int, date, varchar, and enum.
-- 
-- #6 numeric type column in emp_no, salary
-- #7 string type column in first_name, last_name, dept_name, title
-- #8 date type column in birth_date, hire_date, from_date, to_date 
-- 
DESCRIBE dept_emp;
-- #9 They are both inside the employees database.
-- The department table and the employees table both use emp_no
-- Departments can have many employees. An employee could work for
-- multiple deparements. 
-- *** dept_emp links the department table and the employee table through the dept_no. 
-- 
-- #10 SQL used to create the dept_manager table:
SHOW CREATE TABLE dept_manager;
--  CREATE TABLE `dept_manager` (
--   `emp_no` int(11) NOT NULL,
--   `dept_no` char(4) NOT NULL,
--   `from_date` date NOT NULL,
--   `to_date` date NOT NULL,
--   PRIMARY KEY (`emp_no`,`dept_no`),
--   KEY `dept_no` (`dept_no`),
--   CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,
--   CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) REFERENCES `departments` (`dept_no`) ON DELETE CASCADE
-- ) ENGINE=InnoDB DEFAULT CHARSET=latin1

SELECT * FROM mysql.help_topic

