from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.core.db import get_db
from app.core.security import require_jwt
from app.models.recipe import Recipe, RecipeIngredient
from app.schemas.indicators import (
    IndicatorsResponse,
    IngredientCount,
    IngredientBucket,
    RecipeMinItem,
)

router = APIRouter(
    prefix="/indicadores",
    tags=["Indicadores"],
    dependencies=[Depends(require_jwt)],
)

@router.get("", response_model=IndicatorsResponse)
def indicadores(
    db: Session = Depends(get_db),
    top_limit: int = Query(20, ge=1, le=100),
    min_list_limit: int = Query(20, ge=1, le=100),
):
    total_recipes: int = db.execute(select(func.count(Recipe.id))).scalar_one()

    q_top_ing = (
        select(
            RecipeIngredient.ingredient,
            func.count(func.distinct(RecipeIngredient.recipe_id)).label("cnt"),
        )
        .group_by(RecipeIngredient.ingredient)
        .order_by(func.count(func.distinct(RecipeIngredient.recipe_id)).desc(),
                  RecipeIngredient.ingredient.asc())
        .limit(top_limit)
    )
    top_ingredients: List[IngredientCount] = [
        IngredientCount(ingredient=ing, count=cnt)
        for ing, cnt in db.execute(q_top_ing).all()
    ]

    sub_counts = (
        select(
            RecipeIngredient.recipe_id.label("rid"),
            func.count(RecipeIngredient.id).label("n"),
        )
        .group_by(RecipeIngredient.recipe_id)
        .subquery()
    )
    q_hist = (
        select(sub_counts.c.n, func.count().label("recipes"))
        .group_by(sub_counts.c.n)
        .order_by(sub_counts.c.n.asc())
    )
    by_ingredient_count: List[IngredientBucket] = [
        IngredientBucket(ingredients=int(n), recipes=int(rc))
        for n, rc in db.execute(q_hist).all()
    ]

    min_ingredients: int = db.execute(select(func.min(sub_counts.c.n))).scalar_one() or 0

    q_min_list = (
        select(Recipe.id, Recipe.title, sub_counts.c.n)
        .join(sub_counts, sub_counts.c.rid == Recipe.id)
        .where(sub_counts.c.n == min_ingredients)
        .order_by(Recipe.title.asc())
        .limit(min_list_limit)
    )
    recipes_with_min: List[RecipeMinItem] = [
        RecipeMinItem(id=rid, title=title, ingredients=int(n))
        for rid, title, n in db.execute(q_min_list).all()
    ]

    return IndicatorsResponse(
        total_recipes=total_recipes,
        top_ingredients=top_ingredients,
        by_ingredient_count=by_ingredient_count,
        min_ingredients=min_ingredients,
        recipes_with_min=recipes_with_min,
    )
