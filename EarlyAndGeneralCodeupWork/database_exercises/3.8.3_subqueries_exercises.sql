-- Exercises from SQL - Relationships - Subqueries
USE employees;
SHOW TABLES;
-- 1. Find all the employees with the same hire date as employee 101010 
-- using a sub-query. 69 Rows
-- subquery is returning a single row, so use =
SELECT CONCAT(first_name, ' ', last_name) AS full_name,
		hire_date,
        emp_no
FROM employees
WHERE hire_date = 
	  (
		SELECT hire_date
        FROM employees
        WHERE emp_no = 101010
	  )
ORDER BY emp_no;

-- 2. Find all the titles held by all employees with the first name Aamod.
-- 314 total titles, 6 unique titles
-- subquery is returning more than one row, so use IN
SELECT title
FROM titles
WHERE emp_no IN
	   (
		SELECT emp_no
        FROM employees
        WHERE first_name = 'Aamod'
	   );
       
SELECT DISTINCT title
FROM titles
WHERE emp_no IN
	   (
		SELECT emp_no
        FROM employees
        WHERE first_name = 'Aamod'
	   );

-- 3. How many people in the employees table are no longer working for 
-- the company? 59,900
SELECT COUNT(*) AS 'Number of Former Employees'
FROM employees
WHERE emp_no NOT IN(
	SELECT emp_no
	FROM salaries 
    WHERE to_date > NOW()
);

-- 4. Find all the current department managers that are female.
SELECT CONCAT(first_name, ' ', last_name) AS full_name,
		gender
FROM employees
WHERE gender = 'F'
      AND emp_no
				IN(
					SELECT emp_no
					FROM dept_manager
					WHERE to_date > NOW()
	               );

-- 5. Find all the employees that currently have a higher than average 
-- salary.  154543 rows in total. 
SELECT first_name, last_name, salary
FROM employees
JOIN salaries
  ON employees.emp_no = salaries.emp_no
WHERE salaries.to_date > NOW()
  AND salaries.salary > (
					SELECT AVG(salary)
                    FROM salaries)
ORDER BY salary DESC;

-- This would calculate the average from current employees only and give 
-- only current employees whose salaries are higher than that current average
SELECT first_name, last_name, salary
FROM employees
JOIN salaries
  ON employees.emp_no = salaries.emp_no
WHERE salaries.to_date > NOW()
  AND salaries.salary > (
					SELECT AVG(salary)
                    FROM salaries
                    WHERE salaries.to_date > NOW()
                    )
ORDER BY salary DESC;

-- 6. How many current salaries are within 1 standard deviation of the 
-- highest salary? (Hint: you can use a built in function to calculate 
-- the standard deviation.) What percentage of all salaries is this?
-- 78 salaries
SELECT COUNT(salary)
FROM salaries
WHERE salaries.to_date > NOW()
  AND salary >=	
		(SELECT MAX(salary) - STDDEV(salary)
		 FROM salaries
        );
-- What percentage of all salaries is this? .0325%
SELECT 
	(SELECT COUNT(salary)
	 FROM salaries
	 WHERE salaries.to_date > NOW()
	   AND salary >=	
				(SELECT MAX(salary) - STDDEV(salary)
				 FROM salaries
				)
	) 
    / COUNT(salary) * 100
			 FROM salaries
             WHERE to_date > NOW();

-- filtering for current salaries on all yields 83 salaries
SELECT COUNT(salary)
FROM salaries
WHERE salaries.to_date > NOW()
  AND salary >=
		(SELECT MAX(salary) - STDDEV(salary)
		 FROM salaries
         WHERE salaries.to_date > NOW()
        );
-- What percentage of all salaries is this? 0.0346%%
SELECT 
	(SELECT COUNT(salary)
	FROM salaries
	WHERE salaries.to_date > NOW()
		AND salary >=
			(SELECT MAX(salary) - STDDEV(salary)
			FROM salaries
            WHERE salaries.to_date > NOW()
			)
	) 
    / COUNT(salary) * 100
			 FROM salaries
             WHERE to_date > NOW();

-- BONUS:
-- Bonus 1. Find all the department names that currently have female 
-- managers.
SELECT dept_name, CONCAT(first_name, ' ', last_name) AS full_name, gender
FROM departments
JOIN dept_manager
  ON departments.dept_no = dept_manager.dept_no
JOIN employees
  ON dept_manager.emp_no = employees.emp_no
WHERE 
	employees.gender = 'F'
    AND employees.emp_no
			IN(
				SELECT dept_manager.emp_no
				FROM dept_manager
				WHERE dept_manager.to_date > NOW()
	           );

-- same with no JOINS used, but can only print department names
SELECT dept_name
FROM departments
WHERE dept_no IN
	(
		SELECT dept_no
		FROM dept_manager
		WHERE to_date > NOW()
          AND emp_no IN 
				(
				SELECT emp_no
				FROM employees
				WHERE gender = 'F'
				)
	);

-- Bonus 2. Find the first and last name of the employee with the 
-- highest salary. Tokuyasu Pesch $158,220 
SELECT first_name, last_name, salary
FROM employees
JOIN salaries
  ON employees.emp_no = salaries.emp_no
WHERE salaries.to_date > NOW()
  AND salaries.salary IN (
					SELECT MAX(salary)
                    FROM salaries);
-- OR...
SELECT first_name, last_name
FROM employees
WHERE emp_no = 
		(
         SELECT emp_no
         FROM salaries
         ORDER BY salary DESC
         LIMIT 1
         );

-- Bonus 3. Find the department name that the employee with the 
-- highest salary works in. Sales
SELECT first_name, last_name, salary, dept_name
FROM employees
JOIN salaries
  ON employees.emp_no = salaries.emp_no
JOIN dept_emp
  ON employees.emp_no = dept_emp.emp_no
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
WHERE salaries.to_date > NOW()
  AND salaries.salary IN (
					SELECT MAX(salary)
                    FROM salaries);
          
-- or using all subqueries... but gives only department name
SELECT dept_name
FROM departments
WHERE dept_no = 
	(
	SELECT dept_no
	FROM dept_emp
	WHERE emp_no = 
		(
		SELECT emp_no
        FROM employees
        WHERE emp_no = 
			(
			SELECT emp_no
            FROM salaries
            ORDER BY salary DESC
            LIMIT 1
            )
		)
	);