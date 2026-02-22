import { api } from '../../shared/api/client'
import type { CardCreate, CardUpdate, LearningCard } from './types'



export async function getCards(userId: number): Promise<LearningCard[]> {
  const all = await api.get<LearningCard[]>('/learning-cards')
  return all.filter(c => c.user_id === userId)
}

export function createCard(data: CardCreate): Promise<LearningCard> {
  return api.post<LearningCard>('/learning-cards', data)
}

export function updateCard(id: string, data: CardUpdate): Promise<LearningCard> {
  return api.patch<LearningCard>(`/learning-cards/${id}`, data)
}

export function toggleCard(id: string): Promise<LearningCard> {
  return api.post<LearningCard>(`/learning-cards/${id}/toggle`, {})
}

export function deleteCard(id: string): Promise<void> {
  return api.delete(`/learning-cards/${id}`)
}

export function testSendCard(id: string): Promise<{ ok: boolean }> {
  return api.post<{ ok: boolean }>(`/learning-cards/${id}/test-send`, {})
}
