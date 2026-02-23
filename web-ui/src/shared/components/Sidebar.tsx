import { useState } from 'react'
import type { User } from '../../features/auth/types'
import type { Group } from '../../features/groups/types'
import styles from './Sidebar.module.css'

export type Page = 'cards' | 'activity' | 'profile'

interface NavItem {
  id: Page
  icon: string
  label: string
  soon: boolean
}

const NAV: NavItem[] = [
  { id: 'cards',    icon: '📚', label: 'Cards',    soon: false },
  { id: 'activity', icon: '📊', label: 'Activity', soon: true  },
  { id: 'profile',  icon: '⚙️',  label: 'Profile',  soon: true  },
]

interface SidebarProps {
  user: User
  activePage: Page
  onNavigate: (page: Page) => void
  onLogout: () => void
  groups: Group[]
  selectedGroup: number | 'all'
  onSelectGroup: (id: number | 'all') => void
  onAddGroup: (name: string) => Promise<void>
  onDeleteGroup: (id: number) => Promise<void>
}

export function Sidebar({
  user,
  activePage,
  onNavigate,
  onLogout,
  groups,
  selectedGroup,
  onSelectGroup,
  onAddGroup,
  onDeleteGroup,
}: SidebarProps) {
  const initial = user.login.charAt(0).toUpperCase()
  const [addingGroup, setAddingGroup] = useState(false)
  const [newGroupName, setNewGroupName] = useState('')

  async function handleAddGroup() {
    const name = newGroupName.trim()
    if (!name) return
    await onAddGroup(name)
    setNewGroupName('')
    setAddingGroup(false)
  }

  return (
    <aside className={styles.sidebar}>
      <div className={styles.brand}>
        <div className={styles.logoWrap}>🎓</div>
        <span className={styles.appName}>DailyLearn</span>
      </div>

      <nav className={styles.nav}>
        {NAV.map(item => (
          <button
            key={item.id}
            className={`${styles.navItem} ${activePage === item.id ? styles.navItemActive : ''} ${item.soon ? styles.navItemSoon : ''}`}
            onClick={() => !item.soon && onNavigate(item.id)}
            disabled={item.soon}
            title={item.soon ? 'Coming soon' : undefined}
          >
            <span className={styles.navIcon}>{item.icon}</span>
            <span className={styles.navLabel}>{item.label}</span>
            {item.soon && <span className={styles.soonBadge}>Soon</span>}
          </button>
        ))}

        <div className={styles.topicsSection}>
          <span className={styles.topicsLabel}>Topics</span>

          <button
            className={`${styles.topicItem} ${selectedGroup === 'all' ? styles.topicItemActive : ''}`}
            onClick={() => onSelectGroup('all')}
          >
            <span className={styles.topicIcon}>📋</span>
            <span className={styles.topicName}>All Cards</span>
          </button>

          {groups.map(g => (
            <div key={g.id} className={styles.topicRow}>
              <button
                className={`${styles.topicItem} ${selectedGroup === g.id ? styles.topicItemActive : ''}`}
                onClick={() => onSelectGroup(g.id)}
              >
                <span className={styles.topicIcon}>🏷</span>
                <span className={styles.topicName}>{g.name}</span>
              </button>
              <button
                className={styles.topicDelete}
                onClick={() => onDeleteGroup(g.id)}
                title={`Delete "${g.name}"`}
              >
                ×
              </button>
            </div>
          ))}

          {addingGroup ? (
            <div className={styles.topicAddInline}>
              <input
                className={styles.topicInput}
                value={newGroupName}
                onChange={e => setNewGroupName(e.target.value)}
                placeholder="Topic name"
                autoFocus
                onKeyDown={e => {
                  if (e.key === 'Enter') handleAddGroup()
                  if (e.key === 'Escape') { setAddingGroup(false); setNewGroupName('') }
                }}
              />
              <button className={styles.topicAddConfirm} onClick={handleAddGroup}>+</button>
              <button
                className={styles.topicAddCancel}
                onClick={() => { setAddingGroup(false); setNewGroupName('') }}
              >×</button>
            </div>
          ) : (
            <button className={styles.topicAddBtn} onClick={() => setAddingGroup(true)}>
              + New Topic
            </button>
          )}
        </div>
      </nav>

      <div className={styles.userSection}>
        <div className={styles.avatar}>{initial}</div>
        <span className={styles.userLogin}>{user.login}</span>
        <button className={styles.logoutBtn} onClick={onLogout} title="Log out">
          ↩
        </button>
      </div>
    </aside>
  )
}
