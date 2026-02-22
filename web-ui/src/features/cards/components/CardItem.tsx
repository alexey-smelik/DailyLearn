import type { LearningCard } from '../types'
import styles from './CardItem.module.css'

interface CardItemProps {
  card: LearningCard
  onClick: () => void
  onToggle: () => void
  toggling: boolean
}

export function CardItem({ card, onClick, onToggle, toggling }: CardItemProps) {
  return (
    <div
      className={`${styles.card} ${!card.is_active ? styles.inactive : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && onClick()}
    >
      <div className={`${styles.accentBar} ${!card.is_active ? styles.accentBarInactive : ''}`} />
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
      <span className={styles.editHint}>Edit ✎</span>
    </div>
  )
}
