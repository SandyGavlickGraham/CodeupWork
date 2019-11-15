-- Exercises from Functions
USE employees;
SHOW TABLES;
-- 2. Update your queries for employees whose names start and end 
-- with 'E'. Use concat() to combine their first and last name
-- together as a single column named full_name.
SELECT CONCAT(first_name, last_name) AS full_name
FROM employees
WHERE last_name LIKE 'E%' OR last_name LIKE '%E'
ORDER BY emp_no DESC;

-- 3. Convert the names produced in your last query to all 
-- uppercase.
SELECT UPPER(CONCAT(first_name, last_name)) AS full_name
FROM employees
WHERE last_name LIKE 'E%' OR last_name LIKE '%E'
ORDER BY emp_no DESC;

-- 4. For your query of employees born on Christmas and hired 
-- in the 90s, use datediff() to find how many days they 
-- have been working at the company (Hint: You will also 
-- need to use NOW() or CURDATE())
SELECT 
	last_name, 
	first_name, 
	hire_date,
    DATEDIFF(CURDATE(), hire_date) AS num_days_with_company,
    ROUND(DATEDIFF(CURDATE(), hire_date)/365.25, 1) AS num_years_with_company
FROM employees
WHERE hire_date BETWEEN '1990-01-01' AND '1999-12-31'
AND birth_date LIKE '%-12-25'
ORDER BY hire_date DESC;

SELECT 
	last_name, 
	first_name, 
	hire_date,
    DATEDIFF(CURDATE(), hire_date) AS num_days_with_company,
    ROUND(DATEDIFF(CURDATE(), hire_date)/365.25, 1) AS num_years_with_company
FROM employees
ORDER BY ROUND(DATEDIFF(CURDATE(), hire_date)/365.25, 1) DESC;

-- 5. Find the smallest and largest salary from the salaries 
-- table.
SELECT MIN(salary) FROM salaries;
SELECT MAX(salary) FROM salaries;

-- 6. Use your knowledge of built in SQL functions to generate
-- a username for all of the employees. A username should 
-- be all lowercase, and consist of the first character of 
-- the employees first name, the first 4 characters of the 
-- employees last name, an underscore, the month the employee 
-- was born, and the last two digits of the year that they 
-- were born.
SELECT LOWER(CONCAT(SUBSTR(first_name, 1, 1), 
                    SUBSTR(last_name,1, 4), 
                    '_', 
					SUBSTR(birth_date,6,2),
                    SUBSTR(birth_date,3,2))) AS user_name,
		first_name,
        last_name,
        birth_date
FROM employees;