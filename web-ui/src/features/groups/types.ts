export interface Group {
  id: number
  name: string
  user_id: number
}

export interface GroupCreate {
  name: string
  user_id: number
}

export interface GroupUpdate {
  name?: string
}
