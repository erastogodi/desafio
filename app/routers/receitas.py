# app/routers/receitas.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_user
from app.schemas.recipe import RecipesPage, RecipeOut, IngredientOut
from app.repositories.recipe_repo import RecipeRepository

router = APIRouter()

@router.get("/receitas", response_model=RecipesPage)
def list_recipes(
    q: str | None = Query(default=None),
    category: str | None = Query(default=None),
    area: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    repo = RecipeRepository()
    total, items = repo.list(db, q=q, category=category, area=area, limit=limit, offset=offset)

    def to_out(d) -> RecipeOut:
        return RecipeOut(
            id=d["id"],
            source=d["source"],
            title=d["title"],
            url=d["url"],
            published_at=d["published_at"],
            category=d["category"],
            area=d["area"],
            language=d["language"],
            description=d["description"],
            content=d["content"],
            imported_at=d["imported_at"],
            ingredients=[IngredientOut(**ing) for ing in d["ingredients"]],
        )

    return RecipesPage(total=total, items=[to_out(x) for x in items])

@router.get("/receitas/{recipe_id}", response_model=RecipeOut)
def get_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    repo = RecipeRepository()
    d = repo.get_by_id(db, recipe_id)
    if not d:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return RecipeOut(
        id=d["id"],
        source=d["source"],
        title=d["title"],
        url=d["url"],
        published_at=d["published_at"],
        category=d["category"],
        area=d["area"],
        language=d["language"],
        description=d["description"],
        content=d["content"],
        imported_at=d["imported_at"],
        ingredients=[IngredientOut(**ing) for ing in d["ingredients"]],
    )
