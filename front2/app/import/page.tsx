"use client"

import type React from "react"
import { useState } from "react"
import { Navbar } from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { apiClient } from "@/lib/api-client"
import { Download, CheckCircle2 } from "lucide-react"

export default function ImportPage() {
  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess(false)
    setLoading(true)
    try {
      // importa apenas UMA receita por vez
      await apiClient.post("/importar", { q: query, page_size: 1 })
      setSuccess(true)
      setQuery("")
    } catch (err: any) {
      const d = err?.response?.data
      const msg = Array.isArray(d?.detail)
        ? d.detail.map((x: any) => x?.msg || "").join("; ")
        : d?.detail || "Erro ao importar receita"
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2">Importar Receita</h1>
            <p className="text-muted-foreground">Busque e importe uma receita da API externa</p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Download className="h-5 w-5" />
                Importar uma Receita
              </CardTitle>
              <CardDescription>Digite um termo de busca e importe uma única receita</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="query">Termo de Busca</Label>
                  <Input
                    id="query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    required
                    placeholder="Ex: frango, macarrão, banana..."
                  />
                  <p className="text-sm text-muted-foreground">
                    A busca será traduzida automaticamente (ex: “frango” → “chicken”)
                  </p>
                </div>

                {error && (
                  <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
                    {error}
                  </div>
                )}

                {success && (
                  <div className="text-sm text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-950/30 p-3 rounded-md flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4" />
                    Receita importada com sucesso!
                  </div>
                )}

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? "Importando..." : "Importar Receita"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
