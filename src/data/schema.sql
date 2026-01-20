-- schema.sql

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
    start_time timestamp,
    end_time timestamp,
    total_time AS EXTRACT(EPOCH FROM (end_time - start_time)) / 60
    lunchbreak boolean,
    consultant_id INT NOT NULL REFERENCES consultant(id) ON DELETE SET NULL,
    customer_id INT NOT NULL REFERENCES customer(id) ON DELETE SET NULL
);

CREATE MATERIALIZED VIEW total_hours AS
SELECT 
    consultant.id,
    SUM(
      SELECT total_time FROM working_hours WHERE consultant.id = working_hours.consultant_id
      )
FROM consultant
GROUP BY consultant.id;

CREATE TRIGGER update_hours_trigger
AFTER INSERT OR UPDATE OR DELETE ON working_hours
FOR EACH ROW EXECUTE REFRESH MATERIALIZED VIEW CONCURRENTLY total_hours;