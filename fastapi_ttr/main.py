from typing import Optional, List
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from contextlib import asynccontextmanager
import fastapi_swagger_dark as fsd
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from database.database import Base, engine, SessionLocal, get_db
from core.models import PersonModel
from core.schemas import (
    PersonCreateSchema,
    PersonUpdateSchema,
    PersonResponseSchema,
)

# ===== App & Router =====
router = APIRouter()
app = FastAPI(docs_url=None, title="Person API", version="1.0.0")

# ===== Seed initial data =====
initial_persons = [
    {"name": "Alice", "age": 25, "email": "alice@example.com", "password": "password"},
    {"name": "Bob", "age": 30, "email": "bob@example.com", "password": "password"},
    {
        "name": "Charlie",
        "age": 22,
        "email": "charlie@example.com",
        "password": "password",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        if db.query(PersonModel).count() == 0:
            for p in initial_persons:
                person = PersonModel(**p)
                db.add(person)
            db.commit()
    finally:
        db.close()
    yield


app = FastAPI(docs_url=None, title="Person API", version="1.0.0", lifespan=lifespan)


# ===== CRUD Routes =====
@router.get(
    "/persons",
    response_model=List[PersonResponseSchema],
)
def list_persons(
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(PersonModel)
    if q:
        query = query.filter(PersonModel.name.ilike(f"%{q}%"))
    persons = query.order_by(PersonModel.id).all()
    return persons


@router.get("/persons/{person_id}", response_model=PersonResponseSchema)
def get_person(
    person_id: int,
    db: Session = Depends(get_db),
):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.post(
    "/persons", response_model=PersonResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_person(person: PersonCreateSchema, db: Session = Depends(get_db)):
    existing = db.query(PersonModel).filter(PersonModel.email == person.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_person = PersonModel(**person.model_dump())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


@router.patch("/persons/{person_id}", response_model=PersonResponseSchema)
def update_person(
    person_id: int,
    person_update: PersonUpdateSchema,
    db: Session = Depends(get_db),
):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    update_data = person_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(person, key, value)

    db.commit()
    db.refresh(person)
    return person


@router.delete("/persons/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: int,
    db: Session = Depends(get_db),
):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.commit()
    return


# ===== Swagger Dark Theme =====
fsd.install(router, path="/docs")
app.include_router(router)


@app.get("/dark_theme.css", include_in_schema=False, name="dark_theme")
async def dark_theme_css():
    return fsd.dark_swagger_theme


@app.get("/")
def root():
    return {"message": "Welcome to the Person API!"}


# ===== Run =====
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
