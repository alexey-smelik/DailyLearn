import { useState } from 'react'
import type { User } from '../../auth/types'
import { useGroups } from '../../groups/hooks/useGroups'
import { useCards } from '../hooks/useCards'
import type { LearningCard } from '../types'
import { CardForm } from './CardForm'
import { CardItem } from './CardItem'
import styles from './CardGrid.module.css'

interface CardGridProps {
  user: User
  onLogout: () => void
}

export function CardGrid({ user, onLogout }: CardGridProps) {
  const { query, create, update, toggle, remove } = useCards(user.id)
  const groupsHook = useGroups(user.id)
  const [creating, setCreating] = useState(false)
  const [editing, setEditing] = useState<LearningCard | null>(null)
  const [selectedGroup, setSelectedGroup] = useState<number | 'all'>('all')
  const [addingGroup, setAddingGroup] = useState(false)
  const [newGroupName, setNewGroupName] = useState('')

  const allCards = query.data ?? []
  const groups = groupsHook.query.data ?? []
  const initial = user.login.charAt(0).toUpperCase()

  const visibleCards =
    selectedGroup === 'all'
      ? allCards
      : allCards.filter(c => c.group_id === selectedGroup)

  async function handleAddGroup() {
    const name = newGroupName.trim()
    if (!name) return
    await groupsHook.create.mutateAsync({ name, user_id: user.id })
    setNewGroupName('')
    setAddingGroup(false)
  }

  async function handleDeleteGroup(id: number) {
    await groupsHook.remove.mutateAsync(id)
    if (selectedGroup === id) setSelectedGroup('all')
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <div className={styles.logoWrap}>🎓</div>
          <span className={styles.appName}>DailyLearn</span>
        </div>
        <div className={styles.userRow}>
          <div className={styles.avatar}>{initial}</div>
          <span className={styles.userLogin}>{user.login}</span>
          <button className={styles.logoutBtn} onClick={onLogout}>
            Log out
          </button>
        </div>
      </header>

      <main className={styles.main}>
        <div className={styles.toolbar}>
          <div className={styles.headingGroup}>
            <h1 className={styles.heading}>My Cards</h1>
            {allCards.length > 0 && (
              <span className={styles.countBadge}>{allCards.length}</span>
            )}
          </div>
          <button className={styles.addBtn} onClick={() => setCreating(true)}>
            + Add Card
          </button>
        </div>

        {/* Group filter bar */}
        <div className={styles.filterBar}>
          <button
            className={`${styles.filterChip} ${selectedGroup === 'all' ? styles.filterChipActive : ''}`}
            onClick={() => setSelectedGroup('all')}
          >
            All
          </button>
          {groups.map(g => (
            <div key={g.id} className={styles.filterChipWrap}>
              <button
                className={`${styles.filterChip} ${selectedGroup === g.id ? styles.filterChipActive : ''}`}
                onClick={() => setSelectedGroup(g.id)}
              >
                {g.name}
              </button>
              <button
                className={styles.removeGroupBtn}
                onClick={() => handleDeleteGroup(g.id)}
                title={`Delete group "${g.name}"`}
              >
                ×
              </button>
            </div>
          ))}
          {addingGroup ? (
            <div className={styles.addGroupInline}>
              <input
                className={styles.addGroupInput}
                value={newGroupName}
                onChange={e => setNewGroupName(e.target.value)}
                placeholder="Group name"
                autoFocus
                onKeyDown={e => {
                  if (e.key === 'Enter') handleAddGroup()
                  if (e.key === 'Escape') { setAddingGroup(false); setNewGroupName('') }
                }}
              />
              <button className={styles.addGroupConfirm} onClick={handleAddGroup}>Add</button>
              <button className={styles.addGroupCancel} onClick={() => { setAddingGroup(false); setNewGroupName('') }}>×</button>
            </div>
          ) : (
            <button className={styles.newGroupBtn} onClick={() => setAddingGroup(true)}>
              + Group
            </button>
          )}
        </div>

        {query.isLoading && <p className={styles.state}>Loading…</p>}
        {query.isError && <p className={styles.stateError}>Failed to load cards.</p>}

        {!query.isLoading && !query.isError && allCards.length === 0 && (
          <div className={styles.empty}>
            <span className={styles.emptyIcon}>📚</span>
            <p className={styles.emptyTitle}>No cards yet</p>
            <p className={styles.emptyText}>Add your first learning card to get started</p>
            <button className={styles.addBtn} onClick={() => setCreating(true)}>
              + Add Card
            </button>
          </div>
        )}

        {!query.isLoading && !query.isError && allCards.length > 0 && visibleCards.length === 0 && (
          <p className={styles.state}>No cards in this group.</p>
        )}

        {visibleCards.length > 0 && (
          <div className={styles.grid}>
            {visibleCards.map(card => (
              <CardItem
                key={card.id}
                card={card}
                onClick={() => setEditing(card)}
                onToggle={() => toggle.mutateAsync(card.id)}
                toggling={toggle.isPending}
              />
            ))}
          </div>
        )}
      </main>

      {creating && (
        <CardForm
          mode="create"
          userId={user.id}
          groups={groups}
          defaultGroupId={selectedGroup !== 'all' ? selectedGroup : null}
          onSave={data => create.mutateAsync(data)}
          onClose={() => setCreating(false)}
        />
      )}

      {editing && (
        <CardForm
          mode="edit"
          card={editing}
          groups={groups}
          onSave={data => update.mutateAsync({ id: editing.id, data })}
          onDelete={() => remove.mutateAsync(editing.id)}
          onClose={() => setEditing(null)}
        />
      )}
    </div>
  )
}
