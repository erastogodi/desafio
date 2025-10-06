# app/services/recipes_service.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.clients.mealdb_client import MealDBClient
from app.adapters.mealdb_adapter import to_recipe_items
from app.schemas.recipe import RecipeItem
from app.models.recipe import Recipe, RecipeIngredient
from app.utils.i18n import tr, tr_many, tr_to_en


class RecipesService:
    def __init__(self, client: Optional[MealDBClient] = None) -> None:
        self.client = client or MealDBClient()

    def import_from_query(self, db: Session, q: Optional[str], page_size: int = 20) -> List[RecipeItem]:
        # traduz a busca do usuário (pt -> en) para a TheMealDB
        q_en = tr_to_en(q) if q else q

        meals = self.client.search_meals(q_en)
        if not meals:
            return []

        # limita quantidade retornada
        meals = meals[:page_size]

        # adapta payload em RecipeItem
        items = to_recipe_items(meals)

        # traduz campos para PT-BR antes de salvar
        for it in items:
            it.title = tr(it.title) or it.title
            it.category = tr(it.category) if it.category else None
            it.area = tr(it.area) if it.area else None
            it.description = tr(it.description) if it.description else None
            it.content = tr(it.content) if it.content else None

            names = [x.ingredient for x in it.ingredients]
            measures = [x.measure or "" for x in it.ingredients]

            names_pt = tr_many(names)
            measures_pt = tr_many(measures)

            for i, ing in enumerate(it.ingredients):
                ing.ingredient = names_pt[i] or ing.ingredient
                ing.measure = (measures_pt[i] or None)

            it.language = "pt-BR"

        # upsert de receitas + ingredientes
        for it in items:
            recipe = db.get(Recipe, it.id)
            if not recipe:
                recipe = Recipe(
                    id=it.id,
                    source=it.source,
                    title=it.title,
                    url=str(it.url) if it.url is not None else None,
                    published_at=it.published_at,
                    category=it.category,
                    area=it.area,
                    language=it.language,
                    description=it.description,
                    content=it.content,
                )
                db.add(recipe)
            else:
                recipe.source = it.source
                recipe.title = it.title
                recipe.url = str(it.url) if it.url is not None else None
                recipe.published_at = it.published_at
                recipe.category = it.category
                recipe.area = it.area
                recipe.language = it.language
                recipe.description = it.description
                recipe.content = it.content

            recipe.ingredients.clear()
            for ing in it.ingredients:
                recipe.ingredients.append(
                    RecipeIngredient(
                        ingredient=ing.ingredient,
                        measure=ing.measure,
                    )
                )

        db.commit()
        return items
