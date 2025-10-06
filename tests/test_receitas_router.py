from app.models.recipe import Recipe, RecipeIngredient

def seed_recipe(db_session, rid="42"):
    r = Recipe(
        id=rid, source="test", title="Panqueca",
        url="https://example.com/p", category="Sobremesa",
        area="Brasileira", description="Boa", content="Misture tudo"
    )
    r.ingredients.append(RecipeIngredient(ingredient="banana", measure="1"))
    db_session.add(r)
    db_session.commit()
    return r

def test_list_receitas(client, db_session):
    seed_recipe(db_session, rid="42")
    res = client.get("/receitas?limit=50&offset=0")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert any("Panqueca" in x["title"] for x in data["items"])

def test_get_receita_by_id(client, db_session):
    seed_recipe(db_session, rid="99")
    res = client.get("/receitas/99")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "99"
    assert data["ingredients"][0]["ingredient"] == "banana"
