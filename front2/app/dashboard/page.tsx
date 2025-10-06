"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Navbar } from "@/components/navbar"
import RecipeCard from "@/components/recipe-card"
import { apiClient } from "@/lib/api-client"
import { Input } from "@/components/ui/input"
import { Search } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export interface IngredientOut {
  ingredient: string
  measure: string | null
}

export interface RecipeOut {
  id: string
  source: string
  title: string
  url: string
  published_at: string | null
  category: string | null
  area: string | null
  language: string | null
  description: string | null
  content: string | null
  imported_at: string | null
  ingredients: IngredientOut[]
}

/* ---------- Tipos dos indicadores ---------- */
type IndicatorIngredient = { ingredient: string; count: number }
type IndicatorBucket = { ingredients: number; recipes: number }
type IndicatorMinRecipe = { id: string; title: string; ingredients: number }

type IndicatorsResponse = {
  total_recipes: number
  top_ingredients: IndicatorIngredient[]
  by_ingredient_count: IndicatorBucket[]
  min_ingredients: number
  recipes_with_min: IndicatorMinRecipe[]
}

export default function DashboardPage() {
  /* receitas */
  const [recipes, setRecipes] = useState<RecipeOut[]>([])
  const [filtered, setFiltered] = useState<RecipeOut[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")

  /* indicadores */
  const [indLoading, setIndLoading] = useState(true)
  const [indicators, setIndicators] = useState<IndicatorsResponse | null>(null)

  /* carrega receitas */
  useEffect(() => {
    ;(async () => {
      try {
        const res = await apiClient.get("/receitas", { params: { limit: 50, offset: 0 } })
        const items = (res.data?.items ?? []) as RecipeOut[]
        setRecipes(items)
        setFiltered(items)
      } catch (err) {
        console.error("[/receitas] erro:", err)
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  /* carrega indicadores */
  useEffect(() => {
    ;(async () => {
      try {
        const res = await apiClient.get<IndicatorsResponse>("/indicadores")
        setIndicators(res.data)
      } catch (err) {
        console.error("[/indicadores] erro:", err)
      } finally {
        setIndLoading(false)
      }
    })()
  }, [])

  /* filtro de busca */
  useEffect(() => {
    if (!searchTerm) {
      setFiltered(recipes)
      return
    }
    const t = searchTerm.toLowerCase()
    setFiltered(
      recipes.filter(
        (r) =>
          r.title?.toLowerCase().includes(t) ||
          r.category?.toLowerCase().includes(t) ||
          r.area?.toLowerCase().includes(t),
      ),
    )
  }, [searchTerm, recipes])

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Minhas Receitas</h1>
          <p className="text-muted-foreground">Explore e gerencie sua coleção de receitas</p>
        </div>

        {/* Busca */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Buscar por título, categoria ou área..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Indicadores */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Indicadores</h2>

          {indLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-28 bg-muted animate-pulse rounded-lg" />
              ))}
            </div>
          ) : indicators ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Total */}
              <Card>
                <CardHeader>
                  <CardTitle>Total de receitas</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold">{indicators.total_recipes}</p>
                  <p className="text-sm text-muted-foreground">no banco de dados</p>
                </CardContent>
              </Card>

              {/* Top ingredientes */}
              <Card className="lg:col-span-1">
                <CardHeader>
                  <CardTitle>Ingredientes mais usados</CardTitle>
                </CardHeader>
                <CardContent>
                  {indicators.top_ingredients.length === 0 ? (
                    <p className="text-sm text-muted-foreground">Sem dados ainda.</p>
                  ) : (
                    <ul className="text-sm space-y-1">
                      {indicators.top_ingredients.slice(0, 10).map((it) => (
                        <li key={it.ingredient} className="flex justify-between">
                          <span className="truncate">{it.ingredient}</span>
                          <span className="font-medium">{it.count}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>

              {/* Histograma ingredientes/receita */}
              <Card className="lg:col-span-1">
                <CardHeader>
                  <CardTitle>Receitas por nº de ingredientes</CardTitle>
                </CardHeader>
                <CardContent>
                  {indicators.by_ingredient_count.length === 0 ? (
                    <p className="text-sm text-muted-foreground">Sem dados ainda.</p>
                  ) : (
                    <ul className="text-sm space-y-1">
                      {indicators.by_ingredient_count.map((b) => (
                        <li key={b.ingredients} className="flex justify-between">
                          <span>{b.ingredients} ingrediente(s)</span>
                          <span className="font-medium">{b.recipes}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>

              {/* Mínimo + lista */}
              <Card className="lg:col-span-3">
                <CardHeader>
                  <CardTitle>
                    Menor nº de ingredientes:{" "}
                    <span className="font-bold">{indicators.min_ingredients}</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {indicators.recipes_with_min.length === 0 ? (
                    <p className="text-sm text-muted-foreground">Sem receitas nesse bucket.</p>
                  ) : (
                    <ul className="text-sm grid md:grid-cols-2 gap-2">
                      {indicators.recipes_with_min.map((r) => (
                        <li key={r.id} className="flex items-center justify-between">
                          <Link href={`/recipe/${r.id}`} className="text-primary hover:underline">
                            {r.title}
                          </Link>
                          <span className="text-muted-foreground">{r.ingredients} ing.</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </CardContent>
              </Card>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">Não foi possível carregar os indicadores.</p>
          )}
        </section>

        {/* Cards de receitas */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-64 bg-muted animate-pulse rounded-lg" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">
              {searchTerm ? "Nenhuma receita encontrada com esse filtro" : "Nenhuma receita disponível. Importe algumas receitas!"}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((recipe) => (
              <RecipeCard key={recipe.id} recipe={recipe} />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
