"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { apiClient } from "@/lib/api-client"

interface AuthContextType {
  token: string | null
  login: (usernameOrEmail: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const savedToken = localStorage.getItem("token")
    if (savedToken) setToken(savedToken)
  }, [])

  const login = async (usernameOrEmail: string, password: string) => {
    // 👇 backend espera username_or_email
    const res = await apiClient.post("/auth/login", {
      username_or_email: usernameOrEmail,
      password,
    })
    const { access_token } = res.data
    setToken(access_token)
    localStorage.setItem("token", access_token)
  }

  const logout = () => {
    setToken(null)
    localStorage.removeItem("token")
  }

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider")
  return ctx
}
