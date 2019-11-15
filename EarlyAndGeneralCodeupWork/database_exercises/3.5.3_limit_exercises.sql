-- Exercises from SQL - Clauses - Limit
USE employees;
SHOW TABLES;

-- 2. Modify your first query to order by first name. The 
-- first result should be Irena Reutenauer and the 
-- last result should be Vidya Simmen.
SELECT DISTINCT last_name FROM employees
ORDER BY last_name DESC
LIMIT 10;

-- 3. Find your query for employees born on Christmas and 
-- hired in the 90s from order_by_exercises.sql. Update 
-- it to find just the first 5 employees.
SELECT * FROM employees
WHERE hire_date BETWEEN '1990-01-01' AND '1999-12-31'
AND birth_date LIKE '%-12-25'
ORDER BY birth_date, hire_date DESC 
LIMIT 5;

-- 4. Try to think of your results as batches, sets, or 
-- pages. The first five results are your first page. The 
-- five after that would be your second page, etc. 
-- Update the query to find the tenth page of results.
SELECT * FROM employees
WHERE hire_date BETWEEN '1990-01-01' AND '1999-12-31'
AND birth_date LIKE '%-12-25'
ORDER BY birth_date, hire_date DESC 
LIMIT 5 OFFSET 45;
-- Note that 45/5 = 9 so starting at 46 
-- which is on the 10th page

-- LIMIT and OFFSET can be used to create multiple pages 
-- of data. What is the relationship between OFFSET (number 
-- of results to skip), LIMIT (number of results per page), 
-- and the page number?
-- (OFFSET/ LIMIT) + 1 = page number
-- OFFSET = (page number - 1) * LIMIT