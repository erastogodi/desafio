from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field
from pydantic.config import ConfigDict

# ========= MODELOS INTERNOS (usados na importação) =========
class IngredientItem(BaseModel):
    ingredient: str
    measure: Optional[str] = None

class RecipeItem(BaseModel):
    id: str
    source: str
    title: str
    url: HttpUrl
    published_at: Optional[datetime] = None
    category: Optional[str] = None       # ex: "Chicken"
    area: Optional[str] = None           # ex: "Indian"
    language: Optional[str] = None
    description: Optional[str] = None    # Instruções resumidas
    content: Optional[str] = None        # Instruções completas
    ingredients: List[IngredientItem] = Field(default_factory=list)

# ========= PAYLOAD/RESPOSTA DE IMPORTAÇÃO =========
class ImportParams(BaseModel):
    q: Optional[str] = None
    page_size: int = 20

class ImportResponseItem(BaseModel):
    id: str
    source: str
    title: str
    url: HttpUrl
    published_at: Optional[datetime] = None
    category: Optional[str] = None
    area: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    imported_at: Optional[datetime] = None
    ingredients: List[IngredientItem] = Field(default_factory=list)

class ImportResponse(BaseModel):
    imported: int
    items: List[ImportResponseItem]

# ========= SAÍDAS PARA GET =========
class IngredientOut(BaseModel):
    ingredient: str
    measure: Optional[str] = None

class RecipeOut(BaseModel):
    # Permite criação a partir de ORM (.from_orm no v1 / from_attributes no v2)
    model_config = ConfigDict(from_attributes=True)

    id: str
    source: str
    title: str
    url: HttpUrl
    published_at: Optional[datetime] = None
    category: Optional[str] = None
    area: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    imported_at: Optional[datetime] = None
    ingredients: List[IngredientOut] = Field(default_factory=list)

class RecipesPage(BaseModel):
    total: int
    items: List[RecipeOut]
