import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createCard, deleteCard, getCards, toggleCard, updateCard } from '../api'
import type { CardCreate, CardUpdate } from '../types'

export function useCards(userId: number) {
  const qc = useQueryClient()
  const key = ['cards', userId]

  const query = useQuery({
    queryKey: key,
    queryFn: () => getCards(userId),
  })

  const create = useMutation({
    mutationFn: (data: CardCreate) => createCard(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  })

  const update = useMutation({
    mutationFn: ({ id, data }: { id: string; data: CardUpdate }) => updateCard(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  })

  const toggle = useMutation({
    mutationFn: (id: string) => toggleCard(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  })

  const remove = useMutation({
    mutationFn: (id: string) => deleteCard(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  })

  return { query, create, update, toggle, remove }
}
