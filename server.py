from typing import List

import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException, Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from starlette.templating import Jinja2Templates

from employee import Employee
from service import DBService

app = FastAPI()

templates = Jinja2Templates(directory="static")
db_service = DBService('employee.db')

# @app.get("/")
# async def root():
#     return {"message": "Hello World",
#             "message2": "Hello World"}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    all_employees = db_service.get_all_employees()
    # return RedirectResponse(url="/static/index.html")
    return templates.TemplateResponse("index.html", {"request": request, "data": all_employees})


@app.get("/employee", summary="Get all employees", description="Get all employees from sqlite database")
async def get_all_employees() -> List[Employee]:
    all_employees = db_service.get_all_employees()
    return all_employees


@app.get("/employee/{id}", summary="Get one employee by id", description="Get one employee by id from sqlite database")
async def get_one_employee_by_id(id: int) -> Employee:
    # try:
    #     a = None
    #     b = a[0]
    # except TypeError as e:
    #     print(F"Got a typeerror : {e}")
    one_employee = db_service.get_one_employee_by_id(id)
    return one_employee


@app.delete("/employee/{id}", summary="Delete one employee by id",
            description="Delete one employee by id from sqlite database")
async def delete_one_employee_by_id(id: int):
    delete_one_employee_id = db_service.delete_one_employee_by_id(id)
    return delete_one_employee_id


@app.post("/employee/", summary="Create a new employee by firstname, lastname, and pay",
          description="Create a new employee by firstname, lastname, and pay from sqlite database")
async def create_new_employee(employee : Employee):
    create_employee = db_service.create_new_employee(employee)
    return create_employee


@app.put("/employee/{id}", summary="Update values of an employee by his id",
         description="Update values of an employee by his id from sqlite database")
async def update_one_employee_by_id(id: int, employee: Employee):
    if id != employee.id:
        if not employee.id:
            employee.id = id
        else:
            raise HTTPException(status_code=422, detail="Ids mismatch")
    update_an_employee = db_service.update_one_employee_by_id(employee)
    return update_an_employee


uvicorn.run(app, host="0.0.0.0")

# TODO
# delete_one_employee_by_id (pas très compliqué, pas censé retourner un truc, verbe delete)
# create_an_employee (verbe post)
# update_one_employee_by_id (verbe put)
