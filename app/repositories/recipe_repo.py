# app/repositories/recipe_repo.py
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.recipe import Recipe, RecipeIngredient


class RecipeRepository:
    def list(
        self,
        db: Session,
        q: Optional[str] = None,
        category: Optional[str] = None,
        area: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[int, List[Dict[str, Any]]]:
        query = db.query(Recipe).order_by(Recipe.imported_at.desc().nullslast())
        if q:
            query = query.filter(Recipe.title.ilike(f"%{q}%"))
        if category:
            query = query.filter(Recipe.category == category)
        if area:
            query = query.filter(Recipe.area == area)

        total = query.count()
        rows: List[Recipe] = query.offset(offset).limit(limit).all()

        def to_out(r: Recipe) -> Dict[str, Any]:
            return {
                "id": r.id,
                "source": r.source,
                "title": r.title,
                "url": r.url,
                "published_at": r.published_at,
                "category": r.category,
                "area": r.area,
                "language": r.language,
                "description": r.description,
                "content": r.content,
                "imported_at": r.imported_at,
                "ingredients": [
                    {"ingredient": ing.ingredient, "measure": ing.measure}
                    for ing in (r.ingredients or [])
                ],
            }

        return total, [to_out(r) for r in rows]

    def get_by_id(self, db: Session, recipe_id: str) -> Optional[Dict[str, Any]]:
        r: Optional[Recipe] = db.get(Recipe, recipe_id)
        if not r:
            return None
        return {
            "id": r.id,
            "source": r.source,
            "title": r.title,
            "url": r.url,
            "published_at": r.published_at,
            "category": r.category,
            "area": r.area,
            "language": r.language,
            "description": r.description,
            "content": r.content,
            "imported_at": r.imported_at,
            "ingredients": [
                {"ingredient": ing.ingredient, "measure": ing.measure}
                for ing in (r.ingredients or [])
            ],
        }

    def upsert_many(self, db: Session, recipes: List[Dict[str, Any]]) -> int:
        affected = 0
        for it in recipes:
            r = db.get(Recipe, it["id"])
            if not r:
                r = Recipe(
                    id=it["id"],
                    source=it.get("source"),
                    title=it.get("title"),
                    url=str(it.get("url")) if it.get("url") else None,
                    published_at=it.get("published_at"),
                    category=it.get("category"),
                    area=it.get("area"),
                    language=it.get("language"),
                    description=it.get("description"),
                    content=it.get("content"),
                )
                db.add(r)
            else:
                r.source = it.get("source")
                r.title = it.get("title")
                r.url = str(it.get("url")) if it.get("url") else None
                r.published_at = it.get("published_at")
                r.category = it.get("category")
                r.area = it.get("area")
                r.language = it.get("language")
                r.description = it.get("description")
                r.content = it.get("content")

            r.ingredients.clear()
            for ing in it.get("ingredients", []):
                r.ingredients.append(
                    RecipeIngredient(
                        ingredient=ing.get("ingredient"),
                        measure=ing.get("measure"),
                    )
                )

            affected += 1

        db.commit()
        return affected
