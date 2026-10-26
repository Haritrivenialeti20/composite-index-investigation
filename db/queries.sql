-- Baseline query: equality on department, range on salary.
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM employees
WHERE department = 'Sales'
  AND salary > 50000;

-- Second workload query with the same left-most equality column.
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM employees
WHERE department = 'Engineering'
  AND salary >= 70000;

-- Actual result query for application use.
SELECT *
FROM employees
WHERE department = 'Sales'
  AND salary > 50000
ORDER BY salary DESC;

-- After observing the ineffective index, replace it with the query-aligned order.
DROP INDEX IF EXISTS idx_salary_department;
CREATE INDEX idx_department_salary ON employees (department, salary);

-- Re-run both plans after the correction.
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM employees
WHERE department = 'Sales'
  AND salary > 50000;

EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM employees
WHERE department = 'Engineering'
  AND salary >= 70000;
