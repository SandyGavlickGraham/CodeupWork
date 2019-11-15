USE fruits_db;
-- any word that contains a p
SELECT * FROM fruits
WHERE name LIKE '%p%';

-- only words where p is the second letter
SELECT * FROM fruits
WHERE name LIKE '_p%';

-- picking records from a list of options
SELECT * FROM fruits
WHERE name IN ('banana', 'dragonfruit', 'apple');
SELECT * FROM fruits
WHERE name IN ('banana', 'dragonfruit', 'apple')
OR id = 5;
-- AND has a higer order of operation than OR
SELECT * FROM fruits
WHERE name IN ('banana', 'dragonfruit', 'apple')
AND id = 5
OR quantity > 1;
-- but should use parentheses to make order clear
SELECT * FROM fruits
WHERE (name IN ('banana', 'dragonfruit', 'apple')
AND id > 4)
OR quantity > 1;

SELECT * FROM fruits
WHERE name IN ('banana', 'dragonfruit', 'apple')
AND (id > 4 OR quantity > 1);


-- BETWEEN is inclusive
SELECT * FROM fruits
WHERE id BETWEEN 1 AND 3;

