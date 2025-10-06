
from app.services.recipes_service import RecipesService
from app.models.recipe import Recipe


class FakeMealDBClient:
    def search_meals(self, q):
        
        return [
            {
                "idMeal": "100",
                "strMeal": "Chicken Soup",
                "strInstructions": "Mix and cook",
                "strSource": "https://x",
                "strCategory": "Chicken",
                "strArea": "American",
                "strIngredient1": "Chicken",
                "strMeasure1": "200g",
            },
            {
                "idMeal": "200",
                "strMeal": "Banana Pie",
                "strInstructions": "Bake",
                "strSource": "https://y",
                "strCategory": "Dessert",
                "strArea": "American",
                "strIngredient1": "Banana",
                "strMeasure1": "1",
            },
        ]


def test_import_from_query_translates_and_persists(db_session, monkeypatch):

    svc = RecipesService(client=FakeMealDBClient())

    import app.services.recipes_service as svc_mod

  
    monkeypatch.setattr(svc_mod, "tr_to_en", lambda s: "chicken" if s == "frango" else (s or ""))
    monkeypatch.setattr(svc_mod, "tr", lambda s, **kw: f"{s} PT" if s else s)
    monkeypatch.setattr(svc_mod, "tr_many", lambda lst, **kw: [f"{x} PT" if x else x for x in lst])


    items = svc.import_from_query(db_session, q="frango", page_size=10)

    assert len(items) == 2


    r = db_session.get(Recipe, "100")
    assert r is not None
    assert r.title.endswith("PT")
    assert r.language == "pt-BR"
    assert len(r.ingredients) == 1
