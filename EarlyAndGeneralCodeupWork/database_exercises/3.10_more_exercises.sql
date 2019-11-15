USE world;

-- What languages are spoken in Santa Monica?
SELECT countrylanguage.language, countrylanguage.percentage, city.name
FROM countrylanguage
INNER JOIN city
ON countrylanguage.countrycode = city.countrycode
WHERE city.name = 'Santa Monica'
ORDER BY countrylanguage.percentage;

-- How many different countries are in each region?
SELECT region, COUNT(region) AS num_countries
FROM country
GROUP BY region
ORDER BY num_countries;

-- What is the population for each region?
SELECT region AS Region, SUM(population) AS population
FROM country
GROUP BY region
ORDER BY SUM(population) DESC;

-- What is the population for each continent?
SELECT continent AS Continent, SUM(population) AS population
FROM country
GROUP BY continent
ORDER BY SUM(population) DESC;

-- What is the average life expectancy globally? avg(LifeExpectancy) 
SELECT AVG(lifeexpectancy)
FROM country;

-- What is the average life expectancy for each region, each continent? 
-- Sort the results from shortest to longest
SELECT continent, AVG(lifeexpectancy)
FROM country
GROUP BY continent
ORDER BY AVG(lifeexpectancy);

SELECT region, AVG(lifeexpectancy)
FROM country
GROUP BY region
ORDER BY AVG(lifeexpectancy);

-- Find all the countries whose local name is different from the 
-- official name
SELECT name, localname
FROM country
WHERE name != localname;

-- How many countries have a life expectancy less than x?
SELECT name, lifeexpectancy
FROM country
WHERE lifeexpectancy < 40;

-- What state is city x located in? (I took state to mean region.)
SELECT country.name AS country, city.name AS city
FROM country
INNER JOIN city
ON country.code = city.countrycode
WHERE city.name = 'Namibe';

-- What region of the world is city x located in?
SELECT country.region, country.name AS country, city.name AS city
FROM country
INNER JOIN city
ON country.code = city.countrycode
WHERE city.name = 'Namibe';

-- What country (use the human readable name) city x located in?
SELECT country.name AS country, city.name AS city
FROM country
INNER JOIN city
ON country.code = city.countrycode
WHERE city.name = 'Namibe';

-- What is the life expectancy in city x?
SELECT country.name AS country, city.name AS city, country.lifeexpectancy AS life_expectancy
FROM country
INNER JOIN city
ON country.code = city.countrycode
WHERE city.name = 'Namibe';