import { useState } from 'react'
import { ConfirmModal } from '../../../shared/components/ConfirmModal'
import { DuplicateModal } from '../../../shared/components/DuplicateModal'
import type { LearningCard } from '../types'
import styles from './CardItem.module.css'

interface CardItemProps {
  card: LearningCard
  onClick: () => void
  onToggle: () => void
  toggling: boolean
  onDuplicate: (name: string) => void
  onDelete: () => Promise<void>
}

export function CardItem({ card, onClick, onToggle, toggling, onDuplicate, onDelete }: CardItemProps) {
  const [showDuplicate, setShowDuplicate] = useState(false)
  const [showDelete, setShowDelete] = useState(false)
  const [deleteError, setDeleteError] = useState(false)

  return (
    <>
      <div
        className={`${styles.card} ${!card.is_active ? styles.inactive : ''}`}
        onClick={onClick}
        role="button"
        tabIndex={0}
        onKeyDown={e => e.key === 'Enter' && onClick()}
      >
        <div className={`${styles.accentBar} ${!card.is_active ? styles.accentBarInactive : ''}`} />

        {deleteError && (
          <div className={styles.deleteError}>Failed to delete</div>
        )}

        <div className={styles.topActions}>
          <button
            type="button"
            className={styles.deleteBtn}
            onClick={e => { e.stopPropagation(); setShowDelete(true) }}
            title="Delete card"
          >
            🗑
          </button>
          <button
            type="button"
            className={styles.copyBtn}
            onClick={e => { e.stopPropagation(); setShowDuplicate(true) }}
            title="Duplicate card"
          >
            ⎘
          </button>
          <span className={styles.editHint}>Edit ✎</span>
        </div>

        <div className={styles.body}>
          <span className={styles.name}>{card.name}</span>
          <div className={styles.meta}>
            {card.source_url && (
              <a
                className={styles.link}
                href={card.source_url}
                target="_blank"
                rel="noreferrer"
                onClick={e => e.stopPropagation()}
              >
                ↗ Source
              </a>
            )}
            {card.schedule && (
              <span className={styles.schedule}>{card.schedule}</span>
            )}
            <button
              type="button"
              className={`${styles.toggleBtn} ${card.is_active ? styles.toggleBtnActive : styles.toggleBtnPaused}`}
              onClick={e => { e.stopPropagation(); onToggle() }}
              disabled={toggling}
              title={card.is_active ? 'Pause reminders' : 'Resume reminders'}
            >
              {card.is_active ? '● Active' : '○ Paused'}
            </button>
          </div>
        </div>
      </div>

      {showDuplicate && (
        <DuplicateModal
          originalName={card.name}
          onConfirm={name => { onDuplicate(name); setShowDuplicate(false) }}
          onCancel={() => setShowDuplicate(false)}
        />
      )}

      {showDelete && (
        <ConfirmModal
          title="Are you sure you want to delete this card?"
          highlight={card.name}
          description="This action cannot be undone."
          confirmLabel="Delete"
          cancelLabel="Cancel"
          danger
          onConfirm={async () => {
            setShowDelete(false)
            try {
              await onDelete()
            } catch {
              setDeleteError(true)
              setTimeout(() => setDeleteError(false), 3000)
            }
          }}
          onCancel={() => setShowDelete(false)}
        />
      )}
    </>
  )
}
