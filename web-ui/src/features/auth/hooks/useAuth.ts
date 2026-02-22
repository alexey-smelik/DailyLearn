import { useState } from 'react'
import type { User } from '../types'

const STORAGE_KEY = 'dailylearn_user'

function loadUser(): User | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as User) : null
  } catch {
    return null
  }
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(loadUser)

  function login(u: User) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(u))
    setUser(u)
  }

  function logout() {
    localStorage.removeItem(STORAGE_KEY)
    setUser(null)
  }

  return { user, login, logout }
}
