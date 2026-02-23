import { useState } from 'react'
import type { User } from '../../auth/types'
import type { Group } from '../../groups/types'
import { useCards } from '../hooks/useCards'
import type { LearningCard } from '../types'
import { CardForm } from './CardForm'
import { CardItem } from './CardItem'
import styles from './CardGrid.module.css'

interface CardGridProps {
  user: User
  groups: Group[]
  selectedGroup: number | 'all'
}

export function CardGrid({ user, groups, selectedGroup }: CardGridProps) {
  const { query, create, update, toggle, remove } = useCards(user.id)
  const [creating, setCreating] = useState(false)
  const [editing, setEditing] = useState<LearningCard | null>(null)

  const allCards = query.data ?? []

  const visibleCards =
    selectedGroup === 'all'
      ? allCards
      : allCards.filter(c => c.group_id === selectedGroup)

  return (
    <div className={styles.page}>
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
          <p className={styles.state}>No cards in this topic.</p>
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
                onDelete={() => remove.mutateAsync(card.id) as Promise<void>}
                onDuplicate={name => create.mutateAsync({
                  name,
                  source_url: card.source_url ?? undefined,
                  schedule: card.schedule ?? undefined,
                  tg_chat_id: card.tg_chat_id ?? undefined,
                  tg_topic_id: card.tg_topic_id ?? undefined,
                  message_template: card.message_template ?? undefined,
                  group_id: card.group_id,
                  show_pause_button: card.show_pause_button,
                  show_skip_button: card.show_skip_button,
                  show_quiz_button: card.show_quiz_button,
                  time_to_educate: card.time_to_educate ?? undefined,
                  user_id: user.id,
                })}
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
