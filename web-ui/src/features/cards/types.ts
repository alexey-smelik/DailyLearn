export interface LearningCard {
  id: string
  name: string
  source_url: string | null
  schedule: string | null
  tg_chat_id: string | null
  tg_topic_id: number | null
  message_template: string | null
  is_active: boolean
  add_date: string
  group_id: number | null
  user_id: number
}

export interface CardCreate {
  name: string
  source_url?: string
  schedule?: string
  tg_chat_id?: string
  tg_topic_id?: number
  message_template?: string
  group_id?: number | null
  user_id: number
}

export interface CardUpdate {
  name?: string
  source_url?: string | null
  schedule?: string | null
  tg_chat_id?: string | null
  tg_topic_id?: number | null
  message_template?: string | null
  group_id?: number | null
}
