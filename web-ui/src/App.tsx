import { useState } from 'react'
import { LoginModal } from './features/auth/components/LoginModal'
import { useAuth } from './features/auth/hooks/useAuth'
import type { User } from './features/auth/types'
import { useGroups } from './features/groups/hooks/useGroups'
import { CardGrid } from './features/cards/components/CardGrid'
import { Sidebar, type Page } from './shared/components/Sidebar'
import styles from './App.module.css'

function AuthenticatedApp({ user, logout }: { user: User; logout: () => void }) {
  const [page, setPage] = useState<Page>('cards')
  const [selectedGroup, setSelectedGroup] = useState<number | 'all'>('all')
  const groupsHook = useGroups(user.id)
  const groups = groupsHook.query.data ?? []

  async function handleAddGroup(name: string) {
    await groupsHook.create.mutateAsync({ name, user_id: user.id })
  }

  async function handleDeleteGroup(id: number) {
    await groupsHook.remove.mutateAsync(id)
    if (selectedGroup === id) setSelectedGroup('all')
  }

  return (
    <div className={styles.layout}>
      <Sidebar
        user={user}
        activePage={page}
        onNavigate={setPage}
        onLogout={logout}
        groups={groups}
        selectedGroup={selectedGroup}
        onSelectGroup={setSelectedGroup}
        onAddGroup={handleAddGroup}
        onDeleteGroup={handleDeleteGroup}
      />
      <div className={styles.content}>
        {page === 'cards' && (
          <CardGrid
            user={user}
            groups={groups}
            selectedGroup={selectedGroup}
          />
        )}
      </div>
    </div>
  )
}

export function App() {
  const { user, login, logout } = useAuth()

  if (!user) {
    return <LoginModal onLogin={login} />
  }

  return <AuthenticatedApp user={user} logout={logout} />
}
