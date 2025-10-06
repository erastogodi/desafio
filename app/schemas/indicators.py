from pydantic import BaseModel
from typing import List

class IngredientCount(BaseModel):
    ingredient: str
    count: int

class IngredientBucket(BaseModel):
    ingredients: int
    recipes: int

class RecipeMinItem(BaseModel):
    id: str
    title: str
    ingredients: int

class IndicatorsResponse(BaseModel):
    total_recipes: int
    top_ingredients: List[IngredientCount]
    by_ingredient_count: List[IngredientBucket]
    min_ingredients: int
    recipes_with_min: List[RecipeMinItem]
