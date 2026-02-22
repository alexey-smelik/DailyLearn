import { LoginModal } from './features/auth/components/LoginModal'
import { useAuth } from './features/auth/hooks/useAuth'
import { CardGrid } from './features/cards/components/CardGrid'

export function App() {
  const { user, login, logout } = useAuth()

  if (!user) {
    return <LoginModal onLogin={login} />
  }

  return <CardGrid user={user} onLogout={logout} />
}
