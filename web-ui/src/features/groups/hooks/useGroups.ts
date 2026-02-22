import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createGroup, deleteGroup, getGroups, updateGroup } from '../api'
import type { GroupCreate, GroupUpdate } from '../types'

export function useGroups(userId: number) {
  const qc = useQueryClient()
  const key = ['groups', userId]

  const query = useQuery({ queryKey: key, queryFn: () => getGroups(userId) })

  const create = useMutation({
    mutationFn: (data: GroupCreate) => createGroup(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  })

  const update = useMutation({
    mutationFn: ({ id, data }: { id: number; data: GroupUpdate }) => updateGroup(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  })

  const remove = useMutation({
    mutationFn: (id: number) => deleteGroup(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: key })
      // cards may have lost their group_id — refresh cards too
      qc.invalidateQueries({ queryKey: ['cards'] })
    },
  })

  return { query, create, update, remove }
}
