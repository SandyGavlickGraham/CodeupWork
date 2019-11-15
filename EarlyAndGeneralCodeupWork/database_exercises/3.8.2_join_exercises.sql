-- Exercises in SQL - Joined section
USE join_example_db;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM roles;

-- 1. Use the join_example_db. Select all the records 
-- from both the users and roles tables.
SELECT * FROM users JOIN roles ON users.role_id = roles.id;

-- 2. Use join, left join, and right join to combine results
-- from the users and roles tables as we did in the lesson. Before 
-- you run each query, guess the expected number of results.
SELECT * FROM users JOIN roles ON users.role_id = roles.id;
SELECT * FROM users LEFT JOIN roles ON users.role_id = roles.id;
SELECT * FROM users RIGHT JOIN roles ON users.role_id = roles.id;

SELECT * FROM roles JOIN users ON users.role_id = roles.id;
SELECT * FROM roles LEFT JOIN users ON users.role_id = roles.id;
SELECT * FROM roles RIGHT JOIN users ON users.role_id = roles.id;

-- 3. Although not explicitly covered in the lesson, aggregate functions 
-- like count can be used with join queries. Use count and the appropriate 
-- join type to get a list of roles along with the number of users that 
-- has the role. Hint: You will also need to use group by in the query.
SELECT roles.name, COUNT(*) 
FROM roles JOIN users 
ON roles.id = users.role_id
GROUP BY roles.name;

USE employees;
SHOW TABLES;

-- 2. Using the example in the Associative Table Joins section as a guide, 
-- write a query that shows each department along with the name of the
--  current manager for that department.
SELECT * FROM employees LIMIT 3;
SELECT * FROM dept_emp LIMIT 3;
SELECT * FROM departments LIMIT 3;

SELECT departments.dept_name, 
		CONCAT(employees.first_name, ' ', employees.last_name) AS full_name
FROM dept_manager
JOIN departments
  ON dept_manager.dept_no = departments.dept_no
JOIN employees
  ON dept_manager.emp_no = employees.emp_no
WHERE dept_manager.to_date > NOW()
-- WHERE dept_manager.to_date = '9999-01-01'
ORDER BY departments.dept_name;

-- 3. Find the name of all departments currently managed by women.
SELECT departments.dept_name, 
		CONCAT(employees.first_name, ' ', employees.last_name) AS full_name
FROM dept_manager
JOIN departments
  ON dept_manager.dept_no = departments.dept_no
JOIN employees
  ON dept_manager.emp_no = employees.emp_no
WHERE dept_manager.to_date > NOW()
	AND employees.gender = 'F'
ORDER BY departments.dept_name;

-- 4. Find the current titles of employees currently working in the Customer Service department.
SELECT titles.title AS Title, COUNT(*) AS Count
FROM dept_emp
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
JOIN titles
  ON dept_emp.emp_no = titles.emp_no
WHERE departments.dept_name = 'Customer Service'
	AND dept_emp.to_date > NOW()
    AND titles.to_date > NOW()
GROUP BY titles.title
ORDER BY titles.title;

-- 5. Find the current salary of all current managers.
SELECT * FROM salaries LIMIT 100;
SELECT departments.dept_name, 
		CONCAT(employees.first_name, ' ', employees.last_name) AS full_name,
        salaries.salary
FROM dept_manager
JOIN departments
  ON dept_manager.dept_no = departments.dept_no
JOIN employees
  ON dept_manager.emp_no = employees.emp_no
JOIN salaries
  ON dept_manager.emp_no = salaries.emp_no
WHERE dept_manager.to_date > NOW()
	AND salaries.to_date > NOW()
ORDER BY departments.dept_name;

-- 6. Find the number of employees in each department.
SELECT dept_emp.dept_no, departments.dept_name, COUNT(dept_emp.dept_no) AS num_employees
FROM dept_emp
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
WHERE dept_emp.to_date > NOW()
GROUP BY dept_emp.dept_no;

-- 7. Which department has the highest average salary?
SELECT departments.dept_name, ROUND(AVG(salaries.salary)) AS average_salary
FROM dept_emp
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
JOIN salaries
  ON dept_emp.emp_no = salaries.emp_no
WHERE dept_emp.to_date > NOW()
	AND salaries.to_date > NOW()
GROUP BY departments.dept_name
ORDER BY AVG(salaries.salary) DESC 
LIMIT 1;

-- 8. Who is the highest paid employee in the Marketing department?
SELECT employees.first_name, employees.last_name
FROM dept_emp
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
JOIN employees
  ON dept_emp.emp_no = employees.emp_no
JOIN salaries
  ON dept_emp.emp_no = salaries.emp_no
WHERE dept_emp.to_date > NOW()
	AND departments.dept_name = 'Marketing'
ORDER BY salary DESC
LIMIT 1;

-- 9. Which current department manager has the highest salary?
SELECT first_name, last_name, salary, dept_name
FROM dept_manager
JOIN departments
  ON dept_manager.dept_no = departments.dept_no
JOIN employees
  ON dept_manager.emp_no = employees.emp_no
JOIN salaries
  ON dept_manager.emp_no = salaries.emp_no
WHERE dept_manager.to_date > NOW()
	AND salaries.to_date > NOW()
ORDER BY salary DESC
LIMIT 1;

-- 10. Bonus Find the names of all current employees, their 
-- department name, and their current manager's name.
SELECT CONCAT(all_employees.first_name, ' ', all_employees.last_name) AS 'Employee Name', 
       dept_name AS 'Department Name',
       CONCAT(managers.first_name, ' ', managers.last_name) AS 'Manager Name'
FROM dept_emp
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
JOIN employees AS all_employees
  ON dept_emp.emp_no = all_employees.emp_no
LEFT JOIN dept_manager
ON departments.dept_no = dept_manager.dept_no
LEFT JOIN employees AS managers
  ON dept_manager.emp_no = managers.emp_no
WHERE dept_emp.to_date > NOW()
   AND dept_manager.to_date > NOW()
ORDER BY dept_name;

-- 11. Bonus Find the highest paid employee in each department.
SELECT CONCAT(all_employees.first_name, ' ', all_employees.last_name) AS employee_name, 
       dept_name AS 'Department Name',
       salary AS 'Highest Salary in Department'
FROM dept_emp
JOIN employees AS all_employees
  ON dept_emp.emp_no = all_employees.emp_no
JOIN salaries
  ON all_employees.emp_no = salaries.emp_no
JOIN departments
  ON dept_emp.dept_no = departments.dept_no
WHERE dept_emp.to_date > NOW()
   AND salaries.to_date > NOW()
   AND (salary, dept_name) IN (
	SELECT
       MAX(salary), dept_name
       FROM dept_emp
       JOIN salaries
         ON dept_emp.emp_no = salaries.emp_no
       JOIN departments
         ON dept_emp.dept_no = departments.dept_no
	   WHERE dept_emp.to_date > NOW()
		  AND salaries.to_date > NOW()
       GROUP BY dept_name
       )
ORDER BY salary DESC;


-- lists highest salaries in each department
SELECT dept_name,
       MAX(salary) AS 'Highest salary in dept'
       FROM dept_emp
       JOIN salaries
         ON dept_emp.emp_no = salaries.emp_no
       JOIN departments
         ON dept_emp.dept_no = departments.dept_no
       GROUP BY dept_name
       ORDER BY MAX(salary) DESC;