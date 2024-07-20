from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models1, schemas1
from .database import SessionLocal, engine

app = FastAPI()

models1.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/Employee', response_model=schemas1.Employee, tags=['Details of Employee'])
def create_employee(request: schemas1.EmployeeCreate, db: Session = Depends(get_db)):
    emp = models1.Employee(name=request.name, email=request.email, designation=request.designation, payroll=request.payroll)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@app.get('/Employee', response_model=List[schemas1.Employee], tags=['Details of Employee'])
def get_emp(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = db.query(models1.Employee).offset(skip).limit(limit).all()
    return employees

@app.get('/Employee/{Emp_id}', status_code=200, response_model=schemas1.Employee, tags=['Details of Employee'])
def show_employee(employee_id: int, db: Session = Depends(get_db)):
    Employees = db.query(models1.Employee).filter(models1.Employee.id == employee_id).first()
    if not Employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with id {employee_id} not found')
    return Employees

@app.delete('/Employee/{Emp_id}', status_code=status.HTTP_200_OK, tags=['Details of Employee'])
def destroy_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models1.Employee).filter(models1.Employee.id == employee_id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
    return 'Deleted successfully'

@app.put('/Employees/{Emp_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Details of Employee'])
def update_employee(employee_id: int, request: schemas1.EmployeeCreate, db: Session = Depends(get_db)):
    Update = db.query(models1.Employee).filter(models1.Employee.id == employee_id).first()
    if not Update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    for key, value in request.dict().items():
        setattr(Update, key, value)
    db.commit()
    db.refresh(Update)
    return Update



@app.post('/Projects/', response_model=schemas1.Project, tags=['Details of Project'])
def create_project(request: schemas1.ProjectCreate, db: Session = Depends(get_db)):
    Project = models1.Project(title=request.title, description=request.description)
    db.add(Project)
    db.commit()
    db.refresh(Project)
    return Project

@app.get('/Projects/', response_model=List[schemas1.Project], tags=['Details of Project'])
def get_project(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    Getting_projects = db.query(models1.Project).offset(skip).limit(limit).all()
    return Getting_projects

@app.get('/Projects/{Proj_id}', status_code=200, response_model=schemas1.Project, tags=['Details of Project'])
def show_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models1.Project).filter(models1.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Project with id {project_id} not found')
    return project

@app.delete('/Projects/{Proj_id}', status_code=status.HTTP_200_OK, tags=['Details of Project'])
def destroy_project(project_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models1.Project).filter(models1.Project.id == project_id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    return 'Deleted Successfully'

@app.put('/Projects/{Proj_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Details of Project'])
def update_project(project_id: int, request: schemas1.ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(models1.Project).filter(models1.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    for key, value in request.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return 'updated'



@app.post('/Projects/{Proj_id}/Employees/{Emp_id}', tags=['Assignment Projects and Employees'])
def employee_to_project(project_id: int, employee_id: int, db: Session = Depends(get_db)):
    project = db.query(models1.Project).filter(models1.Project.id == project_id).first()
    employee = db.query(models1.Employee).filter(models1.Employee.id == employee_id).first()
    if not project or not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
    project.employees.append(employee)
    db.commit()
    return 'Employee Assigned to project '

@app.post('/Employees/{Emp_id}/Projects/{Proj_id}', tags=['Assignment Projects and Employees'])
def project_to_employee(employee_id: int, project_id: int, db: Session = Depends(get_db)):
    project = db.query(models1.Project).filter(models1.Project.id == project_id).first()
    employee = db.query(models1.Employee).filter(models1.Employee.id == employee_id).first()
    if not project or not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
    employee.projects.append(project)
    db.commit()
    return 'Project assigned to Employee '


@app.get('/Employees/{Emp_id}/Projects', response_model=schemas1.EmployeeWithProjects, tags=['Assignment Projects and Employees'])
def get_employee_project(employee_id: int, db: Session = Depends(get_db)):
    Employee = db.query(models1.Employee).filter(models1.Employee.id == employee_id).first()
    if not Employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return Employee


@app.get('/Projects/{Proj_id}/Employees', response_model=schemas1.ProjectWithEmployees, tags=['Assignment Projects and Employees'])
def get_project_employee(project_id: int, db: Session = Depends(get_db)):
    Project = db.query(models1.Project).filter(models1.Project.id == project_id).first()
    if not Project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return Project
