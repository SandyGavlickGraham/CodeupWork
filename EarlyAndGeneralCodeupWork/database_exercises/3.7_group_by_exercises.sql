-- Exercises from Group By
USE employees;
SHOW TABLES;
-- In your script, use DISTINCT to find the unique titles in the titles table. 
-- Your results should look like:
-- Senior Engineer
-- Staff
-- Engineer
-- Senior Staff
-- Assistant Engineer
-- Technique Leader
-- Manager
SELECT DISTINCT title 
FROM titles;

SELECT title 
FROM titles 
GROUP BY title;

-- Find your query for employees whose last names start and end with 'E'. Update
-- the query find just the unique last names that start and end with 'E' using GROUP BY. 
-- The results should be:
-- Eldridge
-- Erbe
-- Erde
-- Erie
-- Etalle
SELECT last_name
FROM employees
WHERE last_name LIKE 'E%e'
GROUP BY last_name;
-- GROUP BY allows aggregate functions whereas DISTINCT does not
SELECT DISTINCT last_name
FROM employees
WHERE last_name LIKE 'E%e';

-- Update your previous query to now find unique combinations of first and last name 
-- where the last name starts and ends with 'E'. You should get 846 rows.
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS full_name
FROM employees
WHERE last_name LIKE 'E%' AND last_name LIKE '%E'
GROUP BY UPPER(CONCAT(first_name, ' ', last_name));

-- Find the unique last names with a 'q' but not 'qu'. Your results should be:
-- Chleq
-- Lindqvist
-- Qiwen
SELECT last_name
FROM employees
WHERE last_name LIKE '%q%' 
	AND NOT last_name LIKE '%qu%'
GROUP BY last_name;

-- Which (across all employees) name is the most common, the least common? 
-- Find this for both first name, last name, and the combination of the two.
SELECT last_name, COUNT(*)
FROM employees
GROUP BY last_name 
ORDER BY COUNT(last_name) DESC;

SELECT first_name, COUNT(*)
FROM employees
GROUP BY first_name 
ORDER BY COUNT(first_name) DESC;

SELECT CONCAT(first_name, ' ', last_name), COUNT(*)
FROM employees
GROUP BY CONCAT(first_name, ' ', last_name)
ORDER BY COUNT(CONCAT(first_name, ' ', last_name)) DESC;

SELECT first_name, last_name, COUNT(*)
FROM employees
GROUP BY first_name, last_name
ORDER BY COUNT(*) DESC;

-- Update your query for 'Irena', 'Vidya', or 'Maya'. Use COUNT(*) and GROUP BY to find the 
-- number of employees for each gender with those names. Your results should be:
-- 441 M
-- 268 F
SELECT COUNT(gender), gender 
FROM employees
WHERE first_name IN ('Irena', 'Vidya', 'Maya')
GROUP BY gender;

-- Recall the query the generated usernames for the employees from the last lesson. 
-- Are there any duplicate usernames? -- YES!
SELECT COUNT(*) AS name_count, 
       LOWER(CONCAT(SUBSTR(first_name, 1, 1), 
                    SUBSTR(last_name,1, 4), 
                    '_', 
					SUBSTR(birth_date,6,2),
                    SUBSTR(birth_date,3,2))) AS user_name
FROM employees
GROUP BY user_name
ORDER BY COUNT(*) DESC;

-- Bonus: how many duplicate usernames are there? 13,251
SELECT COUNT(*) AS num_of_duplicate_names
FROM (SELECT username, COUNT(*) AS namecount
	  FROM
			(SELECT
				LOWER(CONCAT
						(SUBSTR(first_name, 1, 1), 
						SUBSTR(last_name,1, 4), 
						'_', 
						SUBSTR(birth_date,6,2),
						SUBSTR(birth_date,3,2)
						)
					 ) AS username
			 FROM employees
			) AS required_alias
            
	  GROUP BY username) AS username_counts
WHERE namecount > 1;