"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import Link from "next/link"

type IngredientOut = {
  ingredient: string
  measure: string | null
}

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

type RecipeCardProps = {
  recipe: RecipeOut
}

export default function RecipeCard({ recipe }: RecipeCardProps) {
  const preview =
    recipe.description?.trim() ||
    recipe.content?.slice(0, 140)?.trim() ||
    "Sem descrição."

  const ingPreview = recipe.ingredients?.slice(0, 3)
    .map((ing) => (ing.measure ? `${ing.ingredient} (${ing.measure})` : ing.ingredient))
    .join(" • ")

  return (
    <Card className="h-full flex flex-col">
      <CardContent className="p-4 flex-1 flex flex-col">
        <div className="mb-2">
          <h3 className="font-semibold text-lg leading-snug line-clamp-2">{recipe.title}</h3>
          <div className="mt-2 flex flex-wrap gap-2">
            {recipe.category && <Badge variant="secondary">{recipe.category}</Badge>}
            {recipe.area && <Badge variant="outline">{recipe.area}</Badge>}
          </div>
        </div>

        {ingPreview && (
          <p className="text-sm text-muted-foreground line-clamp-1">
            {ingPreview}{recipe.ingredients.length > 3 ? "…" : ""}
          </p>
        )}

        <p className="mt-2 text-sm text-muted-foreground line-clamp-3">{preview}</p>

        <div className="mt-4">
          <Link href={`/recipe/${recipe.id}`}>
            <Button size="sm" variant="ghost" className="px-0">
              Ver detalhes <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}
