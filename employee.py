from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int | None = Field(default=None, title="Id of the employee")
    first: str = Field(default=None, title="Employee firstname")
    last: str = Field(default=None, title="Employee lastname")
    pay: int = Field(default=None, title="pay")
