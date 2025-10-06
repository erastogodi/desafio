from app.models.recipe import Recipe, RecipeIngredient

def seed_many(db):
    r1 = Recipe(id="1", source="t", title="A", url="https://a")
    r1.ingredients += [
        RecipeIngredient(ingredient="banana", measure=None),
        RecipeIngredient(ingredient="a��car", measure=None),
    ]
    r2 = Recipe(id="2", source="t", title="B", url="https://b")
    r2.ingredients += [RecipeIngredient(ingredient="banana", measure=None)]
    db.add_all([r1, r2]); db.commit()

def test_indicadores(client, db_session):
    seed_many(db_session)
    res = client.get("/indicadores")
    assert res.status_code == 200
    data = res.json()
    assert data["total_recipes"] == 2
    assert data["min_ingredients"] == 1
    assert any(x["ingredient"] == "banana" for x in data["top_ingredients"])
