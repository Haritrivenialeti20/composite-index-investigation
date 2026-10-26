# Index Order Investigation

## Workload

The reporting workload filters employees with an equality predicate on `department` and a range predicate on `salary`:

```sql
WHERE department = 'Sales' AND salary > 50000
```

The second workload uses the same shape for Engineering and a salary threshold of 70,000.

## Original and incorrect index

The starter schema did not create a usable composite index. The experiment first creates the index shown in the lesson's broken example:

```sql
CREATE INDEX idx_salary_department ON employees (salary, department);
```

With this order, the B-tree begins with `salary`. Because the query's first selective equality predicate is on `department`, the planner cannot navigate directly to one department and then scan its salary range. It can only use the salary portion as a range constraint, or choose a sequential scan depending on table statistics and selectivity. The `department` column is not an efficient left-most search key after the salary range.

## Corrected index

The fixed index is:

```sql
CREATE INDEX idx_department_salary ON employees (department, salary);
```

This matches the access pattern: PostgreSQL first narrows the ordered tree to `department = 'Sales'`, then applies the salary range within that department slice. The same shape serves the Engineering query.

## Evidence

`python3 scripts/verify_index_order.py` loads a large deterministic workload and captures query plans before and after the fix. On SQLite, the analogous plans show:

- Wrong order: `SEARCH employees USING COVERING INDEX idx_salary_department (salary>?)` — only the leading salary range is used.
- Correct order: `SEARCH employees USING COVERING INDEX idx_department_salary (department=? AND salary>?)` — both predicates are used.

PostgreSQL may choose a sequential scan for a tiny table or a very unselective predicate, so `EXPLAIN (ANALYZE, BUFFERS)` must always be checked in the real environment. The index order is still structurally correct because it follows the left-most prefix rule and the observed filter pattern.

## Trade-off

The corrected composite index improves these reads but adds write and storage cost. It should not replace every single-column index automatically. The team should monitor `EXPLAIN` output and usage statistics as data distribution changes. The experiment changes indexes only; the employee table structure remains intact.
