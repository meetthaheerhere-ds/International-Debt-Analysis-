CREATE DATABASE IF NOT EXISTS debt_project;
USE debt_project;

-- ---------------- MAIN TABLE ----------------
DROP TABLE IF EXISTS debt_data;

CREATE TABLE debt_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(10),
    series_name TEXT NOT NULL,
    series_code VARCHAR(50),
    year INT NOT NULL,
    value DOUBLE NOT NULL
);

-- ---------------- INDEXES (Performance) ----------------
CREATE INDEX idx_country ON debt_data(country_name);
CREATE INDEX idx_series_code ON debt_data(series_code);
CREATE INDEX idx_year ON debt_data(year);
CREATE INDEX idx_country_year ON debt_data(country_name, year);

-- ---------------- VALIDATION ----------------
SELECT COUNT(*) AS total_records FROM debt_data;
SELECT COUNT(DISTINCT country_name) AS total_countries FROM debt_data;

-- ---------------- ANALYSIS ----------------
SELECT SUM(value) AS total_global_debt FROM debt_data;

SELECT country_name, SUM(value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC;

-- ---------------- VIEW ----------------
DROP VIEW IF EXISTS top_10_countries;

CREATE VIEW top_10_countries AS
SELECT country_name, SUM(value) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;