import { api } from '../../shared/api/client'
import type { Group, GroupCreate, GroupUpdate } from './types'

export function getGroups(userId: number): Promise<Group[]> {
  return api.get<Group[]>('/groups').then(all => all.filter(g => g.user_id === userId))
}

export function createGroup(data: GroupCreate): Promise<Group> {
  return api.post<Group>('/groups', data)
}

export function updateGroup(id: number, data: GroupUpdate): Promise<Group> {
  return api.patch<Group>(`/groups/${id}`, data)
}

export function deleteGroup(id: number): Promise<void> {
  return api.delete(`/groups/${id}`)
}
