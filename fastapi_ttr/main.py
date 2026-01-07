from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import fastapi_swagger_dark as fsd
from core.schemas import *

# ===== App & Router =====
app = FastAPI(docs_url=None, title="Person API", version="1.0.0")
router = APIRouter()

# ===== In-memory DB =====
persons: List[PersonResponseSchema] = [
    PersonResponseSchema(id=1, name="Alice", age=25, email="alice@example.com"),
    PersonResponseSchema(id=2, name="Bob", age=30, email="bob@example.com"),
    PersonResponseSchema(id=3, name="Charlie", age=22, email="charlie@example.com"),
]


def get_person_index(person_id: int) -> int:
    for i, p in enumerate(persons):
        if p.id == person_id:
            return i
    return -1


# ===== Routes =====
@router.get("/persons", response_model=List[PersonResponseSchema])
def list_persons(q: Optional[str] = None):
    results = persons
    if q:
        q_lower = q.lower()
        results = [p for p in persons if q_lower in p.name.lower()]
    return results


@router.get("/persons/{person_id}", response_model=PersonResponseSchema)
def get_person(person_id: int):
    idx = get_person_index(person_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[idx]


@router.post(
    "/persons", response_model=PersonResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_person(person: PersonCreateSchema):
    new_id = max([p.id for p in persons], default=0) + 1
    new_person = PersonResponseSchema(id=new_id, **person.model_dump())
    persons.append(new_person)
    return new_person


@router.patch("/persons/{person_id}", response_model=PersonResponseSchema)
def update_person(person_id: int, person_update: PersonUpdateSchema):
    idx = get_person_index(person_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Person not found")

    existing = persons[idx]
    update_data = person_update.model_dump(exclude_unset=True)
    updated_person = existing.model_copy(update=update_data)
    persons[idx] = updated_person
    return updated_person


@router.delete(
    "/persons/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Person not found"}},
)
def delete_person(person_id: int):
    idx = get_person_index(person_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Person not found")
    persons.pop(idx)
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
