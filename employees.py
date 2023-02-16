import sqlite3

conn = sqlite3.connect('employee.db')

c = conn.cursor()
# c.execute("INSERT INTO employees VALUES (?,?,?)", ('Toto', 'TATa', '20000'))
# conn.commit()
c.execute("SELECT id FROM employees")

print(c.fetchall())

conn.close()