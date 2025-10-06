"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Navbar } from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { apiClient } from "@/lib/api-client"
import { ArrowLeft, MapPin, Tag } from "lucide-react"

type IngredientOut = { ingredient: string; measure: string | null }

type RecipeOut = {
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

export default function RecipeDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [recipe, setRecipe] = useState<RecipeOut | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const id = String(params.id || "")
    if (!id) return
    ;(async () => {
      try {
        const res = await apiClient.get(`/receitas/${id}`)
        setRecipe(res.data as RecipeOut)
      } catch (err) {
        console.error("[/receitas/{id}] erro:", err)
      } finally {
        setLoading(false)
      }
    })()
  }, [params.id])

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto space-y-4">
            <div className="h-8 w-32 bg-muted animate-pulse rounded" />
            <div className="h-12 w-3/4 bg-muted animate-pulse rounded" />
            <div className="h-64 bg-muted animate-pulse rounded" />
          </div>
        </main>
      </div>
    )
  }

  if (!recipe) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto text-center">
            <p className="text-muted-foreground text-lg">Receita não encontrada</p>
            <Button onClick={() => router.push("/dashboard")} className="mt-4">
              Voltar ao Dashboard
            </Button>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Button variant="ghost" onClick={() => router.push("/dashboard")} className="mb-6">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar
          </Button>

          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold mb-4 text-balance">{recipe.title}</h1>
              <div className="flex flex-wrap gap-2">
                {recipe.category && (
                  <Badge variant="secondary" className="flex items-center gap-1">
                    <Tag className="h-3 w-3" />
                    {recipe.category}
                  </Badge>
                )}
                {recipe.area && (
                  <Badge variant="outline" className="flex items-center gap-1">
                    <MapPin className="h-3 w-3" />
                    {recipe.area}
                  </Badge>
                )}
              </div>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Ingredientes</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {recipe.ingredients?.map((ing, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-primary mt-1">•</span>
                      <span>
                        {ing.ingredient}
                        {ing.measure ? ` — ${ing.measure}` : ""}
                      </span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Modo de Preparo</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground leading-relaxed whitespace-pre-wrap">
                  {recipe.content || "Sem instruções disponíveis."}
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
