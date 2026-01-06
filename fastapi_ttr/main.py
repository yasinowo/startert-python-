from fastapi import FastAPI, APIRouter, Request, Depends
import fastapi.responses as responses
import fastapi_swagger_dark as fsd

app = FastAPI(docs_url=None)
router = APIRouter()


@router.get("/names")
async def get_names():
    return [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]


@router.get("/names/{name_id}")
async def get_name(name_id: int):
    names = await get_names()
    for name in names:
        if name["id"] == name_id:
            return name


fsd.install(router, path="/docs")

app.include_router(router)


@app.get("/dark_theme.css", include_in_schema=False, name="dark_theme")
async def dark_theme_css():
    return fsd.dark_swagger_theme


@app.get("/")
def root():
    return {"message": "Welcome to the Name API!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
