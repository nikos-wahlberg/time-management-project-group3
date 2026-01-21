DROP VIEW IF EXISTS total_hours;
DROP TABLE IF EXISTS working_hours;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS consultant;

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    max_allocated_hours INT
);

CREATE TABLE consultant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE working_hours (
    id SERIAL PRIMARY KEY,
    start_time timestamp NOT NULL,
    end_time timestamp NOT NULL,
    lunchbreak boolean,
    total_time FLOAT GENERATED ALWAYS AS (
        (EXTRACT(EPOCH FROM (end_time - start_time)) - 
         CASE 
             WHEN lunchbreak IS TRUE THEN 1800 -- 30 minutes in seconds
             ELSE 0 
         END) / 3600
    ) STORED,
    consultant_id INT NOT NULL REFERENCES consultant(id) ON DELETE SET NULL,
    customer_id INT NOT NULL REFERENCES customer(id) ON DELETE SET NULL
);

CREATE  VIEW total_hours AS
SELECT 
    consultant.name,
    SUM(working_hours.total_time) AS total_worked_hours
FROM consultant
JOIN working_hours ON consultant.id = working_hours.consultant_id
GROUP BY consultant.name;