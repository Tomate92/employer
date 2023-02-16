import sqlite3
import time
from employee import Employee

conn = sqlite3.connect('employee.db')

c = conn.cursor()


# c.execute("""CREATE TABLE employees (
#         id integer PRIMARY KEY AUTOINCREMENT,
#         first text NOT NULL,
#         last text NOT NULL,
#         pay integer NOT NULL
#         )""")

def bijour():
    print("1. Ajouter un employé sur la liste,")
    time.sleep(1.5)
    print("2. Supprimer un employé de la liste,")
    time.sleep(1.5)
    print("3. Modifier le salaire d'un employé,")
    time.sleep(1.5)
    print("4. Visualiser l'ensemble des employés,")
    time.sleep(1.5)
    print("5. Ou bien ne rien faire et arrêter le système ?")
    time.sleep(1.5)


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:id, :first, :last, :pay)",
                  {'id': None, 'first': emp.first, 'last': emp.last, 'pay': emp.pay})
        c.execute("SELECT id FROM employees ORDER BY id DESC LIMIT 1")
        return c.fetchone()

def delete_id(id):
    c.execute("DELETE from employees WHERE id=:id", {'id':id})
    conn.commit()


def get_emps_all():
    c.execute("SELECT * FROM employees")
    return c.fetchall()


def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()

def update_pay_id(pay, id):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE id = :id""",
                  {'pay':pay,'id': id})
        conn.commit()


def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})


print("Bonjour")
time.sleep(1.5)
print("Bienvenue dans le système de gérance des employés.")
time.sleep(01.5)
print("Que voulez-vous faire parmis :")
time.sleep(1.5)
bijour()

g = int(input("(répondre par 1, 2, 3, 4 ou 5) "))

while g != 5:

    if g == 1:
        print()
        print()
        a = input("Quel est le prénom de l'employé ? ")
        b = input("Quel est son nom de famille ? ")
        caa = input("Quel est son salaire Brut par mois ? ")
        emp_1 = Employee(None, str(a), str(b), int(caa))
        inserted = insert_emp(emp_1)
        print(f"Merci d'avoir ajouté l'employé {inserted[0]}.")
        print()
        print("A présent que voulez-vous faire ?")
        bijour()
        g = int(input("(répondre par 1, 2, 3, 4 ou 5) "))






    elif g == 2:
        print()
        print()
        za = str(input("Quel est l'id de l'employé que tu veux retirer de la liste ?"))
        emp_ret = za
        delete_id(emp_ret)
        print()
        bijour()
        g = int(input("(répondre par 1, 2, 3, 4 ou 5) "))




    elif g == 3:
        print()
        print()
        ef = int(input("Quel est l'id de l'employé du changement de salaire ?"))

        er = int(
            input("Par quel nouveau salaire veux-tu changer l'ancien ? "))

        update_pay_id(er, ef)
        print()
        print("A présent que voulez-vous faire ?")
        bijour()
        g = int(input("(répondre par 1, 2, 3, 4 ou 5) "))




    elif g == 4:
        print()
        print()
        emps = get_emps_all()
        for employe in emps:
            print(employe)
        print()
        # print("A présent que voulez-vous faire ?")
        bijour()
        g = int(input("(répondre par 1, 2, 3, 4 ou 5) "))




print()
print()
print("Merci d'avoir utilisé ce système. ")
time.sleep(3)
print()
print("Programme quasi-développé par Thomas")

conn.close()

time.sleep(3)
