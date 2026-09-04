export interface SearchRequest {
  query: string
  province?: string
  doc_type?: string
  year_from?: number
  year_to?: number
  limit?: number
}

export interface SearchResult {
  id: string
  title: string
  section: string
  content: string
  score: number
  doc_type: string
  province: string
  year: number | null
  source_url: string
}

export interface SearchResponse {
  query: string
  verdict: string
  legal_references: SearchResult[]
  steps: string[]
  plain_language: string
  plain_urdu: string
}

export interface Document {
  id: string
  title: string
  title_urdu?: string
  document_type: string
  province: string
  year?: number
  description?: string
  total_sections: number
  source_url?: string
  created_at: string
}

export interface Contributor {
  name: string
  email: string
  phone?: string
  organization?: string
}

export interface Contribution {
  contributor: Contributor
  document_type?: string
  title: string
  content?: string
}
