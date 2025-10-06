from typing import Any, Dict, List, Optional
import httpx

class MealDBClient:
    def __init__(self, base_url: str = "https://www.themealdb.com/api/json/v1/1"):
        self.base_url = base_url.rstrip("/")

    def search_meals(self, q: Optional[str]) -> List[Dict[str, Any]]:
        # /search.php?s=<query> — se q for vazio/None, retornamos lista vazia
        if not q:
            return []
        url = f"{self.base_url}/search.php"
        params = {"s": q}
        with httpx.Client(timeout=20) as client:
            r = client.get(url, params=params)
            r.raise_for_status()
            data = r.json() or {}
            meals = data.get("meals") or []
            return meals
