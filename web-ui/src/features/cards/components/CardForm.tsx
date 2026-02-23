import { useState, type FormEvent } from 'react'
import { Modal } from '../../../shared/components/Modal'
import type { Group } from '../../groups/types'
import type { CardCreate, CardUpdate, LearningCard } from '../types'
import { testSendCard } from '../api'
import { ScheduleBuilder } from './ScheduleBuilder'
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

// Duration quick-picks for the study timer
const DURATION_OPTIONS = [
  { label: '30 min', value: '30m' },
  { label: '1 h',   value: '1h'  },
  { label: '2 h',   value: '2h'  },
  { label: '1 day', value: '1d'  },
  { label: '3 days', value: '3d' },
  { label: '1 week', value: '7d' },
]

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
  const [showPauseButton, setShowPauseButton] = useState(initial?.show_pause_button ?? true)
  const [showSkipButton, setShowSkipButton] = useState(initial?.show_skip_button ?? true)
  const [showQuizButton, setShowQuizButton] = useState(initial?.show_quiz_button ?? false)
  const [timeToEducate, setTimeToEducate] = useState(initial?.time_to_educate ?? '')
  const [conspect, setConspect] = useState(initial?.conspect ?? '')
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
          show_pause_button: showPauseButton,
          show_skip_button: showSkipButton,
          show_quiz_button: showQuizButton,
          time_to_educate: timeToEducate.trim() || undefined,
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
          show_pause_button: showPauseButton,
          show_skip_button: showSkipButton,
          show_quiz_button: showQuizButton,
          time_to_educate: timeToEducate.trim() || null,
          conspect: conspect.trim() || null,
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
    testState === 'ok'      ? 'Sent!'    :
    testState === 'error'   ? 'Failed'   :
    'Test send'

  return (
    <Modal
      title={props.mode === 'create' ? 'New Learning Card' : 'Edit Card'}
      onClose={props.onClose}
    >
      <form onSubmit={handleSubmit} className={styles.form}>

        {/* ── Basic info ───────────────────────────────────────── */}
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

        {props.groups.length > 0 && (
          <label className={styles.label}>
            <span className={styles.labelText}>Topic</span>
            <select
              className={styles.input}
              value={groupId ?? ''}
              onChange={e => setGroupId(e.target.value ? Number(e.target.value) : null)}
              disabled={saving}
            >
              <option value="">— No topic —</option>
              {props.groups.map(g => (
                <option key={g.id} value={g.id}>{g.name}</option>
              ))}
            </select>
          </label>
        )}

        {/* ── Review schedule ──────────────────────────────────── */}
        <div className={styles.label}>
          <span className={styles.labelText}>Review schedule</span>
          <ScheduleBuilder
            value={schedule}
            onChange={setSchedule}
            disabled={saving}
          />
        </div>

        {/* ── Study timer ──────────────────────────────────────── */}
        <div className={styles.label}>
          <span className={styles.labelText}>Study timer</span>
          <div className={styles.durationPicker}>
            {DURATION_OPTIONS.map(opt => (
              <button
                key={opt.value}
                type="button"
                className={`${styles.durationBtn} ${timeToEducate === opt.value ? styles.durationBtnActive : ''}`}
                onClick={() => setTimeToEducate(prev => prev === opt.value ? '' : opt.value)}
                disabled={saving}
              >
                {opt.label}
              </button>
            ))}
            <input
              className={`${styles.input} ${styles.durationCustomInput}`}
              value={DURATION_OPTIONS.some(o => o.value === timeToEducate) ? '' : timeToEducate}
              onChange={e => setTimeToEducate(e.target.value)}
              placeholder="custom (30m, 2h, 3d…)"
              disabled={saving}
            />
          </div>
          <span className={styles.hint}>
            After this delay Telegram will ask you to write study notes for this card.
          </span>
        </div>

        {/* ── Telegram notifications ───────────────────────────── */}
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

        {/* ── Study notes (edit only) ──────────────────────────── */}
        {props.mode === 'edit' && (
          <>
            <p className={styles.sectionTitle}>Study notes</p>
            <label className={styles.label}>
              <span className={styles.labelText}>Conspect</span>
              <textarea
                className={`${styles.input} ${styles.textarea}`}
                value={conspect}
                onChange={e => setConspect(e.target.value)}
                placeholder="Your study notes will appear here after you respond in Telegram…"
                disabled={saving}
                rows={5}
              />
              {props.card.conspect_requested && !props.card.conspect && (
                <span className={styles.hint}>Conspect request sent — waiting for your Telegram reply.</span>
              )}
            </label>
          </>
        )}

        {/* ── Inline buttons ───────────────────────────────────── */}
        <p className={styles.sectionTitle}>Inline buttons</p>
        <div className={styles.toggleRow}>
          <label className={styles.toggleLabel}>
            <span className={styles.toggleSwitch}>
              <input
                type="checkbox"
                className={styles.toggleInput}
                checked={showPauseButton}
                onChange={e => setShowPauseButton(e.target.checked)}
                disabled={saving}
              />
              <span className={styles.toggleTrack} />
            </span>
            <span>⏸ Pause</span>
          </label>
          <label className={styles.toggleLabel}>
            <span className={styles.toggleSwitch}>
              <input
                type="checkbox"
                className={styles.toggleInput}
                checked={showSkipButton}
                onChange={e => setShowSkipButton(e.target.checked)}
                disabled={saving}
              />
              <span className={styles.toggleTrack} />
            </span>
            <span>⏭ Skip</span>
          </label>
          <label className={styles.toggleLabel}>
            <span className={styles.toggleSwitch}>
              <input
                type="checkbox"
                className={styles.toggleInput}
                checked={showQuizButton}
                onChange={e => setShowQuizButton(e.target.checked)}
                disabled={saving}
              />
              <span className={styles.toggleTrack} />
            </span>
            <span>
              🧠 Quiz
              {showQuizButton && !conspect && (
                <span className={styles.hint}> — shown only when notes exist</span>
              )}
            </span>
          </label>
        </div>

        <div className={styles.divider} />

        {/* ── Actions ──────────────────────────────────────────── */}
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
