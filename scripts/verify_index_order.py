from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[1]
conn = sqlite3.connect(':memory:')
conn.execute('PRAGMA automatic_index = OFF')
conn.execute('''CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary NUMERIC NOT NULL,
    hire_date TEXT NOT NULL
)''')

# Use enough deterministic rows for the planner to expose the index prefix behavior.
rows=[]
for i in range(50000):
    departments=('Sales','Engineering','HR','Finance','Support')
    department=departments[i % len(departments)]
    salary=35000 + ((i * 7919) % 90000)
    rows.append((i+1, f'Employee {i+1}', department, salary, '2020-01-15'))
conn.executemany('INSERT INTO employees VALUES (?, ?, ?, ?, ?)', rows)
conn.execute('CREATE INDEX idx_salary_department ON employees (salary, department)')
query="SELECT * FROM employees WHERE department = 'Sales' AND salary > 50000"
wrong=conn.execute('EXPLAIN QUERY PLAN '+query).fetchall()
wrong_text=' | '.join(row[3] for row in wrong)
assert 'idx_salary_department' in wrong_text and 'salary>?' in wrong_text
conn.execute('DROP INDEX idx_salary_department')
conn.execute('CREATE INDEX idx_department_salary ON employees (department, salary)')
correct=conn.execute('EXPLAIN QUERY PLAN '+query).fetchall()
correct_text=' | '.join(row[3] for row in correct)
assert 'idx_department_salary' in correct_text and 'department=?' in correct_text and 'salary>?' in correct_text

print('wrong index plan:    ', wrong_text)
print('correct index plan:  ', correct_text)
print('sales results:       ', conn.execute(query).fetchone() is not None)
print('verification passed: corrected order uses the equality prefix and salary range')
(root/'docs/query-plans.txt').write_text(
    'Wrong index (salary, department):\n' + wrong_text +
    '\n\nCorrect index (department, salary):\n' + correct_text + '\n'
)
