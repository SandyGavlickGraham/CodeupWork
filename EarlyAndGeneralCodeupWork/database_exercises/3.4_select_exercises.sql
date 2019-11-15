SHOW DATABASES;
-- Use the albums_db database.
USE albums_db;
-- Explore the structure of the albums table.
SHOW TABLES;

-- Write queries to find the following information.
-- The name of all albums by Pink Floyd
SELECT name FROM albums 
	WHERE artist = 'Pink Floyd';
-- The Dark Side of the Moon
-- The Wall

-- The year Sgt. Pepper's Lonely Hearts Club Band was released
SELECT release_date FROM albums 
	WHERE name = 'Sgt. Pepper''s Lonely Hearts Club Band';
-- 1967

-- The genre for the album Nevermind
SELECT genre FROM albums 
	WHERE name = 'Nevermind';
-- Grunge, Alternative rock

-- Which albums were released in the 1990s
SELECT name, release_date 
	FROM albums 
	WHERE release_date BETWEEN '1990' AND '1999';
-- The Bodyguard 1992
-- Jagged Little Pill 1995
-- Come On Over 1997
-- Falling into You 1996
-- Let's Talk About Love 1997
-- Dangerous 1991
-- The Immaculate Collection 1990
-- Titanic: Music from the Motion Picture 1997
-- Metallica 1991
-- Nevermind 1991
-- Supernatural 1999

-- Which albums had less than 20 million certified sales
SELECT name, sales FROM albums 
	WHERE sales < 20;
-- Grease: The original soundtrack 14.4
-- Bad 19.3
-- Sgt. Pepper's Lonely Hearts Club Band 13.1
-- Dirty Dancing 17.9
-- Let's Talk About Love 19.3
-- Dangerous 16.3
-- The Immaculate Collection 19.4
-- Abbey Road 14.4
-- Born in the U.S.A 19.6
-- Brothers in Arms 17.7
-- Titanic: Music from the Motion Picture 18.1
-- Nevermind 16.7
-- The Wall 17.6

-- All the albums with a genre of "Rock". Why do these query results not include albums with a genre of "Hard rock" or "Progressive rock"?
SELECT name, genre FROM albums 
	WHERE genre = 'Rock' 
		OR genre = 'Hard rock' 
		OR genre = 'Progressive rock';
-- or can use LIKE...
SELECT name, genre 
    FROM albums 
	WHERE genre LIKE '%Rock%';
-- If you only specify 'Rock', it will 
-- not give you the strings in which rock is a subset.
-- Back in Black -- Hard Rock
-- The Dark Side of the Moon -- Progressive rock
-- Sgt. Pepper's Lonely Hearts Club Band -- Rock
-- 1 -- Rock
-- Abbey Road -- Rock
-- Born in the U.S.A. -- Rock
-- The Wall -- Progressive rock
-- Supernatural -- Rock
-- Appetite for Destruction -- Hard rock 

-- Write a query that shows all the information in the `help_topic` table in the
-- `mysql` database. 
SELECT * FROM mysql.help_topic;
-- How could you write a query to search for a specific help topic?
-- example:
-- IF @WholeString LIKE '%' + @ExpressionToFind + '%'  
--    PRINT 'Found it'  
-- ELSE  
--    PRINT 'Did not find it'  
-- but how do I make that pull from the mysql.help.topic table?

-- Take a look at the information in the salaries table in the employees
-- database. What do you notice?
-- in salary table of employee database: 
--             emp_no, salary, from_date, to_date

-- Explore the `sakila` database. What do you think this database represents?
USE sakila;
SHOW TABLES;
-- sakila table contains actors and what movies they 
--             were in as well as many other details.

-- What kind of company might be using this database?
-- A company involved in awarding lifetime achievement awards?

-- write a query that shows all the columns from the `actors` table
SELECT * FROM actor;

-- write a query that only shows the last name of the actors from the `actors` table
SELECT last_name FROM actor;

-- Write a query that displays the title, description, rating, movie length
SELECT title, description, rating, length FROM film;

-- columns from the `films` table for films that last 3 hours or longer.
SELECT * FROM film WHERE length > 180;

-- Select the payment id, amount, and payment date columns from the payment
-- table for payments made on or after 05/27/2005.
SELECT payment_id, amount, payment_date FROM payment
	WHERE payment_date > '2005-05-27';

-- Select the primary key, amount, and payment date columns from the payment
-- table for payments made on 05/27/2005.
SELECT COUNT(*) FROM payment 
       WHERE payment_date BETWEEN '2005-05-27' AND '2005-05-28';
       -- 167 records
SELECT payment_id, amount, payment_date FROM payment 
       WHERE payment_date BETWEEN '2005-05-27' AND '2005-05-28';