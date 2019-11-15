-- Exercise from SQL - Clauses - WHERE
USE employees;
SHOW TABLES;

-- 2. Find all employees with first names 'Irena', 
-- 'Vidya', or 'Maya' — 709 rows (Hint: Use IN).
SELECT * FROM employees
WHERE first_name IN ('Irena', 'Vidya', 'Maya');

-- 3. Find all employees whose last name starts with 'E' 
-- 7,330 rows.
SELECT * FROM employees
WHERE last_name LIKE 'E%';

-- 4. Find all employees hired in the 90s — 135,214 rows.
SELECT * FROM employees
WHERE hire_date LIKE '199%';

-- 5. Find all employees born on Christmas — 842 rows.
-- note that adding the first dash is optional, but makes it more clear that
-- the code is pulling a date
SELECT * FROM employees
WHERE birth_date LIKE '%-12-25';

-- 6. Find all employees with a 'q' in their last name 
-- 1,873 rows.
SELECT * FROM employees
WHERE last_name LIKE '%q%';

-- 1. Update your query for 'Irena', 'Vidya', or 'Maya' 
-- to use OR instead of IN — 709 rows.
SELECT * FROM employees
WHERE first_name = 'Irena' OR first_name = 'Vidya' OR first_name = 'Maya';
SELECT * FROM employees
WHERE first_name IN ('Irena', 'Vidya', 'Maya');

-- 2. Add a condition to the previous query to find 
-- everybody with those names who is also male — 441 rows.
SELECT * FROM employees
WHERE first_name IN ('Irena', 'Vidya', 'Maya')
AND gender = 'M';
-- if use ORs, then need to use parentheses or the AND only sticks to Maya
-- using IN is better, though
SELECT * FROM employees
WHERE (first_name = 'Irena' OR first_name = 'Vidya' OR first_name = 'Maya')
AND gender = 'M';

-- 3. Find all employees whose last name starts or ends 
-- with 'E' — 30,723 rows.
SELECT * FROM employees
WHERE last_name LIKE 'E%' OR last_name LIKE '%E';

-- 4. Duplicate the previous query and update it to find 
-- all employees whose last name starts and ends with 'E' 
-- 899 rows.
SELECT * FROM employees
WHERE last_name LIKE 'E%' AND last_name LIKE '%E';
-- better...
SELECT * FROM employees
WHERE last_name LIKE 'E%e';

-- 5. Find all employees hired in the 90s and born on 
-- Christmas — 362 rows.
SELECT * FROM employees
WHERE hire_date LIKE '199%' AND birth_date LIKE '%-12-25';
-- or to clarify that the hire_date is a date...
SELECT * FROM employees
WHERE hire_date BETWEEN '1990-01-01' AND '1999-12-31'
AND birth_date LIKE '%-12-25';

-- 6. Find all employees with a 'q' in their last name 
-- but not 'qu' — 547 rows.
SELECT * FROM employees
WHERE last_name LIKE '%q%' 
AND NOT last_name LIKE '%qu%';