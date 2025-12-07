from fastapi import APIRouter, Depends

from database import SessionDep
from schemas.example_schema import Example
from repos import example_repo

router = APIRouter(tags=["example"],prefix="/example")

@router.get("/example", response_model=Example)
async def get_example(db: SessionDep):
    return await example_repo.get_example(db)
