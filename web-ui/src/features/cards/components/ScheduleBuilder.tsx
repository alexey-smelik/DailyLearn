import { useState } from 'react'
import styles from './ScheduleBuilder.module.css'

interface Interval {
  value: number
  unit: 'm' | 'h' | 'd'
}

const PRESETS = [
  {
    id: 'ebbinghaus',
    label: 'Ebbinghaus',
    hint: 'Classic: 1d · 3d · 7d · 14d · 30d · 90d',
    intervals: [
      { value: 1,  unit: 'd' as const },
      { value: 3,  unit: 'd' as const },
      { value: 7,  unit: 'd' as const },
      { value: 14, unit: 'd' as const },
      { value: 30, unit: 'd' as const },
      { value: 90, unit: 'd' as const },
    ],
  },
  {
    id: 'fast',
    label: 'Fast',
    hint: 'Simpler material: 1d · 2d · 5d · 14d · 30d',
    intervals: [
      { value: 1,  unit: 'd' as const },
      { value: 2,  unit: 'd' as const },
      { value: 5,  unit: 'd' as const },
      { value: 14, unit: 'd' as const },
      { value: 30, unit: 'd' as const },
    ],
  },
  {
    id: 'deep',
    label: 'Deep',
    hint: 'Complex material: 7d · 14d · 30d · 60d · 180d',
    intervals: [
      { value: 7,   unit: 'd' as const },
      { value: 14,  unit: 'd' as const },
      { value: 30,  unit: 'd' as const },
      { value: 60,  unit: 'd' as const },
      { value: 180, unit: 'd' as const },
    ],
  },
]

function toMinutes(iv: Interval): number {
  if (iv.unit === 'm') return iv.value
  if (iv.unit === 'h') return iv.value * 60
  return iv.value * 1440
}

function formatCumulative(minutes: number): string {
  if (minutes < 60) return `${minutes}m`
  if (minutes < 1440) return `${Math.round(minutes / 60)}h`
  return `Day ${Math.round(minutes / 1440)}`
}

function parseString(s: string): Interval[] {
  const RE = /(\d+)\s*(m|h|d)/gi
  const out: Interval[] = []
  let m: RegExpExecArray | null
  while ((m = RE.exec(s)) !== null) {
    out.push({ value: parseInt(m[1], 10), unit: m[2].toLowerCase() as 'm' | 'h' | 'd' })
  }
  return out
}

function toString(ivs: Interval[]): string {
  return ivs.map(iv => `${iv.value}${iv.unit}`).join(' → ')
}

function detectPreset(ivs: Interval[]): string | null {
  for (const p of PRESETS) {
    if (p.intervals.length !== ivs.length) continue
    if (p.intervals.every((piv, i) => piv.value === ivs[i].value && piv.unit === ivs[i].unit)) {
      return p.id
    }
  }
  return null
}

interface Props {
  value: string
  onChange: (v: string) => void
  disabled?: boolean
}

export function ScheduleBuilder({ value, onChange, disabled }: Props) {
  const [intervals, setIntervals] = useState<Interval[]>(() => {
    const parsed = value ? parseString(value) : []
    return parsed.length ? parsed : [...PRESETS[0].intervals]
  })
  const [isCustom, setIsCustom] = useState<boolean>(() => {
    const parsed = value ? parseString(value) : (PRESETS[0].intervals as Interval[])
    return !detectPreset(parsed)
  })
  const [editingIdx, setEditingIdx] = useState<number | null>(null)
  const [editDraft, setEditDraft] = useState('')

  const activePresetId = isCustom ? null : detectPreset(intervals)

  function applyIntervals(next: Interval[]) {
    setIntervals(next)
    onChange(toString(next))
  }

  function applyPreset(id: string) {
    const p = PRESETS.find(p => p.id === id)!
    applyIntervals([...p.intervals])
    setIsCustom(false)
    setEditingIdx(null)
  }

  function commitEdit(idx: number) {
    const parsed = parseString(editDraft)
    if (parsed.length) {
      const next = [...intervals]
      next[idx] = parsed[0]
      applyIntervals(next)
    }
    setEditingIdx(null)
  }

  function removeChip(idx: number) {
    applyIntervals(intervals.filter((_, i) => i !== idx))
  }

  function addChip() {
    const last = intervals[intervals.length - 1]
    const newIv: Interval = last
      ? { value: Math.min(last.value * 2, 365), unit: last.unit }
      : { value: 1, unit: 'd' }
    const next = [...intervals, newIv]
    applyIntervals(next)
    setEditingIdx(next.length - 1)
    setEditDraft(`${newIv.value}${newIv.unit}`)
  }

  function beginEdit(idx: number) {
    if (!isCustom || disabled) return
    setEditingIdx(idx)
    setEditDraft(`${intervals[idx].value}${intervals[idx].unit}`)
  }

  const cumulative = (() => {
    let total = 0
    return intervals.map(iv => { total += toMinutes(iv); return total })
  })()

  return (
    <div className={styles.root}>

      {/* ── Preset pills ─────────────────────────────────────────── */}
      <div className={styles.presets}>
        {PRESETS.map(p => (
          <button
            key={p.id}
            type="button"
            className={`${styles.presetBtn} ${activePresetId === p.id ? styles.presetBtnActive : ''}`}
            onClick={() => applyPreset(p.id)}
            disabled={disabled}
            title={p.hint}
          >
            {p.label}
          </button>
        ))}
        <button
          type="button"
          className={`${styles.presetBtn} ${isCustom ? styles.presetBtnActive : ''}`}
          onClick={() => setIsCustom(true)}
          disabled={disabled}
          title="Define your own intervals"
        >
          Custom
        </button>
      </div>

      {/* ── Interval chips ───────────────────────────────────────── */}
      <div className={styles.chips}>
        {intervals.map((iv, idx) => (
          <div key={idx} className={styles.chipGroup}>
            {editingIdx === idx ? (
              <input
                className={styles.chipInput}
                value={editDraft}
                onChange={e => setEditDraft(e.target.value)}
                onBlur={() => commitEdit(idx)}
                onKeyDown={e => {
                  if (e.key === 'Enter' || e.key === 'Tab') { e.preventDefault(); commitEdit(idx) }
                  if (e.key === 'Escape') setEditingIdx(null)
                }}
                autoFocus
                placeholder="3d"
              />
            ) : (
              <button
                type="button"
                className={`${styles.chip} ${isCustom && !disabled ? styles.chipEditable : ''}`}
                onClick={() => beginEdit(idx)}
                title={isCustom ? 'Click to edit' : undefined}
              >
                {iv.value}{iv.unit}
                {isCustom && !disabled && (
                  <span
                    className={styles.chipX}
                    role="button"
                    onClick={e => { e.stopPropagation(); removeChip(idx) }}
                  >
                    ×
                  </span>
                )}
              </button>
            )}
            {idx < intervals.length - 1 && <span className={styles.arrow}>→</span>}
          </div>
        ))}
        {isCustom && !disabled && (
          <button type="button" className={styles.addChip} onClick={addChip}>
            + add
          </button>
        )}
      </div>

      {/* ── Cumulative timeline ──────────────────────────────────── */}
      {intervals.length > 0 && (
        <div className={styles.timeline}>
          {cumulative.map((cum, idx) => (
            <div key={idx} className={styles.timelineItem}>
              <div className={styles.timelineDot} />
              <span className={styles.timelineDate}>{formatCumulative(cum)}</span>
            </div>
          ))}
        </div>
      )}

      {isCustom && (
        <span className={styles.customHint}>
          Supported units: <code>m</code> minutes · <code>h</code> hours · <code>d</code> days
        </span>
      )}
    </div>
  )
}
