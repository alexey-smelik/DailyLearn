import { useEffect, useState } from 'react'
import styles from './DuplicateModal.module.css'

interface DuplicateModalProps {
  originalName: string
  onConfirm: (name: string) => void
  onCancel: () => void
}

export function DuplicateModal({ originalName, onConfirm, onCancel }: DuplicateModalProps) {
  const [name, setName] = useState(`Copy of ${originalName}`)

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCancel()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onCancel])

  function handleConfirm() {
    const trimmed = name.trim()
    if (!trimmed) return
    onConfirm(trimmed)
  }

  return (
    <div className={styles.backdrop} onClick={onCancel}>
      <div className={styles.panel} onClick={e => e.stopPropagation()}>

        <div className={styles.iconWrap}>⎘</div>

        <h2 className={styles.title}>Duplicate card</h2>

        <p className={styles.originalLabel}>Copying from</p>
        <p className={styles.originalName}>"{originalName}"</p>

        <div className={styles.field}>
          <label className={styles.fieldLabel}>New card name</label>
          <input
            className={styles.input}
            value={name}
            onChange={e => setName(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleConfirm()}
            autoFocus
            placeholder="Enter a name…"
          />
        </div>

        <div className={styles.actions}>
          <button type="button" className={styles.cancelBtn} onClick={onCancel}>
            Cancel
          </button>
          <button
            type="button"
            className={styles.confirmBtn}
            onClick={handleConfirm}
            disabled={!name.trim()}
          >
            Duplicate
          </button>
        </div>

      </div>
    </div>
  )
}
