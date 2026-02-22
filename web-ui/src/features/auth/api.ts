import { api } from '../../shared/api/client'
import type { User } from './types'

export async function getOrCreateUser(login: string): Promise<User> {
  const users = await api.get<User[]>('/users')
  const existing = users.find(u => u.login === login)
  if (existing) return existing
  return api.post<User>('/users', { login })
}
