export interface LearningCard {
  id: string
  name: string
  source_url: string | null
  schedule: string | null
  tg_chat_id: string | null
  tg_topic_id: number | null
  message_template: string | null
  is_active: boolean
  show_pause_button: boolean
  show_skip_button: boolean
  show_quiz_button: boolean
  time_to_educate: string | null
  conspect: string | null
  conspect_requested: boolean
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
  show_pause_button?: boolean
  show_skip_button?: boolean
  show_quiz_button?: boolean
  time_to_educate?: string
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
  show_pause_button?: boolean | null
  show_skip_button?: boolean | null
  show_quiz_button?: boolean | null
  time_to_educate?: string | null
  conspect?: string | null
}
