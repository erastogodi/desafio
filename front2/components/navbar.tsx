"use client"

import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { useAuth } from "@/context/auth-context"
import { ChefHat, LogOut, Home, Download } from "lucide-react"

export function Navbar() {
  const { logout } = useAuth()
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.push("/login")
  }

  return (
    <nav className="border-b border-border bg-card">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Link href="/dashboard" className="flex items-center gap-2 font-bold text-lg">
              <div className="p-2 bg-primary rounded-lg">
                <ChefHat className="h-5 w-5 text-primary-foreground" />
              </div>
              <span>Painel de Receitas</span>
            </Link>
            <div className="hidden md:flex items-center gap-4">
              <Link href="/dashboard">
                <Button variant="ghost" size="sm" className="gap-2">
                  <Home className="h-4 w-4" />
                  Dashboard
                </Button>
              </Link>
              <Link href="/import">
                <Button variant="ghost" size="sm" className="gap-2">
                  <Download className="h-4 w-4" />
                  Importar
                </Button>
              </Link>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <Button variant="ghost" size="sm" onClick={handleLogout} className="gap-2">
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Sair</span>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
