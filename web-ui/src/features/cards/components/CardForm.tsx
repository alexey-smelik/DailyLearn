import { useState, type FormEvent } from 'react'
import { Modal } from '../../../shared/components/Modal'
import type { Group } from '../../groups/types'
import type { CardCreate, CardUpdate, LearningCard } from '../types'
import { testSendCard } from '../api'
import styles from './CardForm.module.css'

interface CreateProps {
  mode: 'create'
  userId: number
  groups: Group[]
  defaultGroupId?: number | null
  onSave: (data: CardCreate) => void
  onClose: () => void
}

interface EditProps {
  mode: 'edit'
  card: LearningCard
  groups: Group[]
  onSave: (data: CardUpdate) => void
  onDelete: () => void
  onClose: () => void
}

type CardFormProps = CreateProps | EditProps

export function CardForm(props: CardFormProps) {
  const initial = props.mode === 'edit' ? props.card : null

  const [name, setName] = useState(initial?.name ?? '')
  const [sourceUrl, setSourceUrl] = useState(initial?.source_url ?? '')
  const [schedule, setSchedule] = useState(initial?.schedule ?? '')
  const [tgChatId, setTgChatId] = useState(initial?.tg_chat_id ?? '')
  const [tgTopicId, setTgTopicId] = useState(
    initial?.tg_topic_id != null ? String(initial.tg_topic_id) : ''
  )
  const [messageTemplate, setMessageTemplate] = useState(initial?.message_template ?? '')
  const [groupId, setGroupId] = useState<number | null>(
    initial?.group_id ?? (props.mode === 'create' ? (props.defaultGroupId ?? null) : null)
  )
  const [saving, setSaving] = useState(false)
  const [testState, setTestState] = useState<'idle' | 'sending' | 'ok' | 'error'>('idle')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setSaving(true)
    try {
      const topicId = tgTopicId.trim() ? parseInt(tgTopicId.trim(), 10) : undefined
      if (props.mode === 'create') {
        await props.onSave({
          name: name.trim(),
          source_url: sourceUrl.trim() || undefined,
          schedule: schedule.trim() || undefined,
          tg_chat_id: tgChatId.trim() || undefined,
          tg_topic_id: topicId,
          message_template: messageTemplate.trim() || undefined,
          group_id: groupId,
          user_id: props.userId,
        })
      } else {
        await props.onSave({
          name: name.trim(),
          source_url: sourceUrl.trim() || null,
          schedule: schedule.trim() || null,
          tg_chat_id: tgChatId.trim() || null,
          tg_topic_id: topicId ?? null,
          message_template: messageTemplate.trim() || null,
          group_id: groupId,
        })
      }
      props.onClose()
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (props.mode !== 'edit') return
    setSaving(true)
    try {
      await props.onDelete()
      props.onClose()
    } finally {
      setSaving(false)
    }
  }

  async function handleTestSend() {
    if (props.mode !== 'edit') return
    setTestState('sending')
    try {
      await testSendCard(props.card.id)
      setTestState('ok')
      setTimeout(() => setTestState('idle'), 3000)
    } catch {
      setTestState('error')
      setTimeout(() => setTestState('idle'), 3000)
    }
  }

  const testLabel =
    testState === 'sending' ? 'Sending…' :
    testState === 'ok' ? 'Sent!' :
    testState === 'error' ? 'Failed' :
    'Test send'

  return (
    <Modal
      title={props.mode === 'create' ? 'New Learning Card' : 'Edit Card'}
      onClose={props.onClose}
    >
      <form onSubmit={handleSubmit} className={styles.form}>
        <label className={styles.label}>
          <span className={styles.labelText}>Name *</span>
          <input
            className={styles.input}
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="e.g. React hooks"
            autoFocus
            disabled={saving}
          />
        </label>

        <label className={styles.label}>
          <span className={styles.labelText}>Source URL</span>
          <input
            className={styles.input}
            value={sourceUrl}
            onChange={e => setSourceUrl(e.target.value)}
            placeholder="https://..."
            disabled={saving}
          />
        </label>

        <label className={styles.label}>
          <span className={styles.labelText}>Schedule</span>
          <input
            className={styles.input}
            value={schedule}
            onChange={e => setSchedule(e.target.value)}
            placeholder="e.g. 1d → 3d → 7d → 30d"
            disabled={saving}
          />
        </label>

        {props.groups.length > 0 && (
          <label className={styles.label}>
            <span className={styles.labelText}>Group</span>
            <select
              className={styles.input}
              value={groupId ?? ''}
              onChange={e => setGroupId(e.target.value ? Number(e.target.value) : null)}
              disabled={saving}
            >
              <option value="">— No group —</option>
              {props.groups.map(g => (
                <option key={g.id} value={g.id}>{g.name}</option>
              ))}
            </select>
          </label>
        )}

        <p className={styles.sectionTitle}>Telegram notifications</p>

        <div className={styles.row}>
          <label className={`${styles.label} ${styles.grow}`}>
            <span className={styles.labelText}>Chat ID</span>
            <input
              className={styles.input}
              value={tgChatId}
              onChange={e => setTgChatId(e.target.value)}
              placeholder="-100123456789"
              disabled={saving}
            />
          </label>
          <label className={styles.label}>
            <span className={styles.labelText}>Topic ID</span>
            <input
              className={`${styles.input} ${styles.narrow}`}
              value={tgTopicId}
              onChange={e => setTgTopicId(e.target.value)}
              placeholder="optional"
              disabled={saving}
            />
          </label>
        </div>

        <label className={styles.label}>
          <span className={styles.labelText}>Message template</span>
          <textarea
            className={`${styles.input} ${styles.textarea}`}
            value={messageTemplate}
            onChange={e => setMessageTemplate(e.target.value)}
            placeholder="e.g. Time to review: {{name}}"
            disabled={saving}
            rows={3}
          />
          <span className={styles.hint}>
            Variables: <code>{'{{name}}'}</code> <code>{'{{source_url}}'}</code> <code>{'{{schedule}}'}</code>
          </span>
        </label>

        <div className={styles.divider} />

        <div className={styles.actions}>
          {props.mode === 'edit' && (
            <button
              type="button"
              className={styles.deleteBtn}
              onClick={handleDelete}
              disabled={saving}
            >
              Delete
            </button>
          )}
          <div className={styles.rightActions}>
            {props.mode === 'edit' && (
              <button
                type="button"
                className={`${styles.testBtn} ${testState === 'ok' ? styles.testBtnOk : ''} ${testState === 'error' ? styles.testBtnError : ''}`}
                onClick={handleTestSend}
                disabled={saving || testState === 'sending' || !props.card.tg_chat_id}
                title={!props.card.tg_chat_id ? 'Set Chat ID first' : 'Send a test Telegram message'}
              >
                {testLabel}
              </button>
            )}
            <button
              type="submit"
              className={styles.saveBtn}
              disabled={saving || !name.trim()}
            >
              {saving ? 'Saving…' : 'Save card'}
            </button>
          </div>
        </div>
      </form>
    </Modal>
  )
}
