-- Temporary Tables exercises

-- 1. Using the example from the lesson, re-create the 
-- employees_with_departments table.
USE ada_661;
SHOW TABLES;
DROP TABLE employees_with_departments;

CREATE TABLE employees_with_departments AS
SELECT emp_no, first_name, last_name, dept_no, dept_name
FROM employees.employees
JOIN employees.dept_emp USING(emp_no)
JOIN employees.departments USING(dept_no)
LIMIT 100;

-- 1a. Add a column named full_name to this table. It should be a VARCHAR 
-- whose length is the sum of the lengths of the first name and last name
-- columns
ALTER TABLE employees_with_departments 
ADD full_name VARCHAR(31);
DESCRIBE employees_with_departments;

-- 1b. Update the table so that full name column contains the correct data
UPDATE employees_with_departments
SET full_name = 
	CONCAT(first_name, ' ', last_name);
DESCRIBE employees_with_departments;

-- 1c. Remove the first_name and last_name columns from the table.
ALTER TABLE employees_with_departments 
DROP COLUMN first_name;
ALTER TABLE employees_with_departments 
DROP COLUMN last_name;
DESCRIBE employees_with_departments;

-- 1d. What is another way you could have ended up with this same table?
CREATE TABLE employees_with_departments_2 AS
SELECT emp_no, 
	   CONCAT(first_name, ' ', last_name) AS full_name, 
       dept_no, 
       dept_name
FROM employees.employees
JOIN employees.dept_emp USING(emp_no)
JOIN employees.departments USING(dept_no)
LIMIT 100;
DESCRIBE employees_with_departments_2;

-- 2. Create a temporary table based on the payments table from the sakila 
-- database.

CREATE TABLE temporary_sakila AS
SELECT payment_id, 
	   customer_id,
       staff_id,
       rental_id,
       amount,
       payment_date,
       last_update
FROM sakila.payment;
DESCRIBE temporary_sakila;

-- Write the SQL necessary to transform the amount column such that it is 
-- stored as an integer representing the number of cents of the payment. 
-- For example, 1.99 should become 199.
SELECT amount FROM temporary_sakila ORDER BY amount DESC;

ALTER TABLE temporary_sakila 
ADD cents INT(8);

UPDATE temporary_sakila
SET cents = amount * 100;

SELECT cents FROM temporary_sakila ORDER BY amount DESC;

-- 3. Find out how the average pay in each department compares to the 
-- overall average pay. In order to make the comparison easier, you should
-- use the Z-score for salaries. In terms of salary, what is the best 
-- department to work for? The worst?
USE ada_661;
SHOW TABLES;
DESCRIBE employees_with_departments_and_salaries;

CREATE TABLE employees_with_departments_and_salaries 
SELECT emp_no, 
	   CONCAT(first_name, ' ', last_name) AS full_name, 
       dept_no, 
       dept_name,
       salary
FROM employees.employees
JOIN employees.dept_emp USING(emp_no)
JOIN employees.departments USING(dept_no)
JOIN employees.salaries USING(emp_no)
WHERE employees.dept_emp.to_date > NOW()
  AND employees.salaries.to_date > NOW();
  
DESCRIBE employees_with_departments_and_salaries;

-- overall average salary
SELECT AVG(salary)
FROM employees_with_departments_and_salaries;

-- standard deviation of all
SELECT STDDEV(salary)
FROM employees_with_departments_and_salaries;

-- z-scores for sales department
SELECT emp_no,
	   (salary - 
		   (SELECT AVG(salary) FROM employees_with_departments_and_salaries)
	   )
	   /
	   (SELECT STDDEV(salary) FROM employees_with_departments_and_salaries)
FROM employees_with_departments_and_salaries 
WHERE dept_name = 'Sales';

-- create temp table for z_scores
SHOW TABLES;

CREATE TABLE z_scores_table AS
SELECT emp_no, full_name, dept_no, dept_name,
	   (salary - 
		   (SELECT AVG(salary) FROM employees_with_departments_and_salaries)
	   )
	   /
	   (SELECT STDDEV(salary) FROM employees_with_departments_and_salaries) AS emp_z_score
FROM employees_with_departments_and_salaries;

DESCRIBE z_scores_table;

SELECT *
FROM z_scores_table
LIMIT 5;

-- COULD NOT GET TO WORK SO INSTEAD ADDED ALL NECESSARY DATA TO z_scores_table
-- add z-scores from temp table to z_scores column
-- UPDATE employees_with_departments_and_salaries
-- SET z_scores = z_scores_table.emp_z_score;
    
-- average z-score by department
SELECT dept_name, AVG(emp_z_score) AS dept_z_score_avg
FROM z_scores_table
GROUP BY dept_name
ORDER BY dept_z_score_avg DESC;

-- So now answer question...
-- 3. Find out how the average pay in each department compares to the 
-- overall average pay. In order to make the comparison easier, you should
-- use the Z-score for salaries. In terms of salary, what is the best 
-- department to work for? The worst?
-- Sales is best because its salaries have an average standard deviation of
-- 0.97 above the overall average salary.
-- My results match the average salary by dept, so that's confirmation that I'm not totally off-base!
SELECT dept_name, AVG(salary)
FROM employees_with_departments_and_salaries
GROUP BY dept_name
ORDER BY AVG(salary) DESC;

-- 4. What is the average salary for an employee based on the number of 
-- years they have been with the company? Express your answer in terms of 
-- the Z-score of salary.
-- Since this data is a little older, scale the years of experience by 
-- subtracting the minumum from every row.
SELECT ROUND((DATEDIFF(NOW(), hire_date)) / 365.25) - 19 AS years_with_company,
	   AVG(emp_z_score) AS salary_z_score
FROM employees.employees
JOIN z_scores_table USING (emp_no)
GROUP BY years_with_company;