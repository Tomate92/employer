import sqlite3
from typing import List

from fastapi import HTTPException

from employee import Employee


class DBService:

    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def get_employees_ids(self):
        self.c.execute("SELECT id FROM employees")
        return self.c.fetchall()

    # def get_emps_others(self):
    #     self.c.execute("SELECT first, last, pay FROM employees")
    #     return self.c.fetchall()

    def get_all_employees(self) -> List[Employee]:
        self.c.execute("SELECT * FROM employees")
        all_employees_tuples = self.c.fetchall()

        all_employees = list()

        for emp in all_employees_tuples:
            employee = Employee(id=emp[0], first=emp[1], last=emp[2], pay=emp[3])
            all_employees.append(employee)

        return all_employees

    def get_one_employee_by_id(self, id: int) -> Employee:
        self.c.execute("SELECT * FROM employees WHERE id=:id", {'id': id})
        emp = self.c.fetchone()
        if not emp:
            raise HTTPException(status_code=404, detail="Item not found")
        employee = Employee(id=emp[0], first=emp[1], last=emp[2], pay=emp[3])

        return employee

    def delete_one_employee_by_id(self, id: int):
        self.c.execute("DELETE from employees WHERE id=:id", {'id': id})
        self.conn.commit()

    def create_new_employee(self, employee: Employee) -> Employee:
        self.c.execute("INSERT INTO employees VALUES (:id, :first, :last, :pay)",
                       {'id': None, 'first': employee.first, 'last': employee.last, 'pay': employee.pay})
        self.conn.commit()
        new_id = self.c.execute("SELECT id FROM employees ORDER BY id DESC LIMIT 1").fetchone()
        new_employee = self.get_one_employee_by_id(new_id[0])
        return new_employee

    def update_one_employee_by_id(self, employee: Employee) -> Employee:
        self.c.execute("""UPDATE employees SET pay = :pay, first=:first, last=:last
                    WHERE id = :id""",
                       {'pay': employee.pay, 'id': employee.id, 'first': employee.first, 'last': employee.last})
        self.conn.commit()
        return self.get_one_employee_by_id(employee.id)

    def delete_all_employees(self):
        self.c.execute("DELETE * from employees")
        self.conn.commit()
