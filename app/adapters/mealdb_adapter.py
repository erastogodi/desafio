from typing import Any, Dict, List
from app.schemas.recipe import RecipeItem, IngredientItem

def _join_nonempty(parts: List[str], sep: str = " ") -> str:
    return sep.join([p for p in parts if p])

def _collect_ingredients(meal: Dict[str, Any]) -> List[IngredientItem]:
    out: List[IngredientItem] = []
    # TheMealDB expõe até 20 pares strIngredientN / strMeasureN
    for i in range(1, 21):
        ing = (meal.get(f"strIngredient{i}") or "").strip()
        meas = (meal.get(f"strMeasure{i}") or "").strip()
        if not ing:
            continue
        out.append(IngredientItem(ingredient=ing, measure=meas or None))
    return out

def to_recipe_items(meals: List[Dict[str, Any]]) -> List[RecipeItem]:
    items: List[RecipeItem] = []
    for m in meals:
        # Descrição curta: primeiras linhas de instruções
        instructions = (m.get("strInstructions") or "").strip()
        small_desc = "\n".join(instructions.splitlines()[:8]) if instructions else None

        
        full_content = instructions or None

        
        url = (m.get("strSource") or m.get("strYoutube") or m.get("strMealThumb") or "").strip()

        item = RecipeItem(
            id=str(m.get("idMeal")),
            source="themealdb",
            title=(m.get("strMeal") or "").strip(),
            url=url,  # Pydantic HttpUrl valida
            published_at=None,  # não há data real na API
            category=(m.get("strCategory") or None),
            area=(m.get("strArea") or None),
            language=None,
            description=small_desc,
            content=full_content,
            ingredients=_collect_ingredients(m),
        )
        items.append(item)
    return items
