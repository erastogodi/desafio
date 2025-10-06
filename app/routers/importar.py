from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import get_current_user  # se estiver usando auth
from app.schemas.recipe import ImportParams, ImportResponse, ImportResponseItem, IngredientItem
from app.services.recipes_service import RecipesService
from app.clients.mealdb_client import MealDBClient

router = APIRouter()

@router.post("/importar", response_model=ImportResponse)
def importar(
    body: ImportParams,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    svc = RecipesService(client=MealDBClient())
    items = svc.import_from_query(db, body.q, body.page_size)

    def to_resp_item(it) -> ImportResponseItem:
        return ImportResponseItem(
            id=it.id,
            source=it.source,
            title=it.title,
            url=it.url,
            published_at=it.published_at,
            category=it.category,
            area=it.area,
            language=it.language,
            description=it.description,
            content=it.content,
            imported_at=None, 
            ingredients=[IngredientItem(ingredient=x.ingredient, measure=x.measure) for x in it.ingredients],
        )

    resp_items = [to_resp_item(it) for it in items]
    return ImportResponse(imported=len(resp_items), items=resp_items)
