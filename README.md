# Composite Index Investigation

This project investigates why a composite index can exist yet fail to support a multi-column reporting query. The workload is an employee report filtered by an equality predicate on `department` and a range predicate on `salary`.

## Query

```sql
SELECT *
FROM employees
WHERE department = 'Sales'
  AND salary > 50000;
```

A second Engineering query with the same predicate shape is included in `db/queries.sql`.

## Experiment

The experiment first creates the ineffective order:

```sql
CREATE INDEX idx_salary_department ON employees (salary, department);
```

The query starts with `department`, but this index starts with `salary`. Under the left-most prefix rule, the planner cannot efficiently navigate to one department and then apply the salary range. The captured plan uses only the salary range portion.

The corrected index is:

```sql
CREATE INDEX idx_department_salary ON employees (department, salary);
```

Now the equality column is first and the range column is second. The captured plan uses both `department=?` and `salary>?` in the index search. The query-plan comparison is in `docs/query-plan-comparison.png`, with raw output in `docs/query-plans.txt`.

## Verification

Run:

```bash
python3 scripts/verify_index_order.py
```

The harness loads 50,000 deterministic employee rows, disables automatic indexes, runs `EXPLAIN QUERY PLAN` with the wrong index, drops it, creates the corrected index, and verifies the before/after access paths. For PostgreSQL, run the statements in `db/queries.sql` with `EXPLAIN (ANALYZE, BUFFERS)` and compare the actual plan chosen by the production statistics.

## Trade-off

The corrected index improves these reads but consumes storage and adds write maintenance. Index order should follow real filter patterns and be confirmed with `EXPLAIN`; a sequential scan can still be correct for a tiny table or an unselective predicate. The employee table structure remains unchanged, as required by the challenge.
