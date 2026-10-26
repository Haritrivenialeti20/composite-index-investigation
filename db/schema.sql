-- Employee reporting workload used for the index-order experiment.
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC NOT NULL,
    hire_date DATE NOT NULL
);

-- The intentionally ineffective experiment index.
CREATE INDEX IF NOT EXISTS idx_salary_department
    ON employees (salary, department);
