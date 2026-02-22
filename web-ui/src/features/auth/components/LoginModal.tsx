import { useState, type FormEvent } from 'react'
import { Modal } from '../../../shared/components/Modal'
import { getOrCreateUser } from '../api'
import type { User } from '../types'
import styles from './LoginModal.module.css'

interface LoginModalProps {
  onLogin: (user: User) => void
}

export function LoginModal({ onLogin }: LoginModalProps) {
  const [login, setLogin] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const trimmed = login.trim()
    if (!trimmed) return
    setLoading(true)
    setError('')
    try {
      const user = await getOrCreateUser(trimmed)
      onLogin(user)
    } catch {
      setError('Could not connect to server. Make sure the API is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal title="">
      <div className={styles.hero}>
        <span className={styles.heroIcon}>🎓</span>
        <h1 className={styles.heroTitle}>DailyLearn</h1>
        <p className={styles.heroSub}>Your spaced repetition workspace</p>
      </div>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div>
          <label className={styles.fieldLabel}>Login</label>
          <div className={styles.inputWrap}>
            <span className={styles.inputIcon}>👤</span>
            <input
              className={styles.input}
              type="text"
              placeholder="your-login"
              value={login}
              onChange={e => setLogin(e.target.value)}
              autoFocus
              disabled={loading}
            />
          </div>
        </div>

        {error && <p className={styles.error}>⚠ {error}</p>}

        <button className={styles.button} type="submit" disabled={loading || !login.trim()}>
          {loading ? 'Connecting…' : 'Enter workspace →'}
        </button>
      </form>
    </Modal>
  )
}
