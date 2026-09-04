import { useSearchParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { SearchBar } from '../components/SearchBar'
import { LegalReference } from '../components/LegalReference'
import { ActionSteps } from '../components/ActionSteps'

interface SearchResult {
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

interface SearchResponse {
  query: string
  verdict: string
  legal_references: SearchResult[]
  steps: string[]
  plain_language: string
  plain_urdu: string
}

export function Results() {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q') || ''
  const [result, setResult] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (query) {
      setLoading(true)
      api.post('/api/v1/search', { query })
        .then((res) => setResult(res.data))
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false))
    }
  }, [query])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 py-6">
        <div className="container mx-auto px-4">
          <SearchBar />
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin h-12 w-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-gray-600">Searching legal database...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {error}
          </div>
        )}

        {result && (
          <>
            <div className="card mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">The Verdict</h2>
              <p className="text-lg text-gray-700">{result.verdict}</p>
            </div>

            <div className="card mb-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Plain Language Explanation</h3>
              <p className="text-gray-700 whitespace-pre-line">{result.plain_language}</p>
            </div>

            {result.plain_urdu && (
              <div className="card mb-6 border-r-4 border-primary-500">
                <h3 className="text-xl font-bold text-gray-900 mb-4">اردو میں سادہ زبان</h3>
                <p className="text-gray-700 whitespace-pre-line text-right" dir="rtl">{result.plain_urdu}</p>
              </div>
            )}

            <div className="card mb-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Legal References</h3>
              <div className="space-y-4">
                {result.legal_references.map((ref) => (
                  <LegalReference key={ref.id} reference={ref} />
                ))}
              </div>
            </div>

            {result.steps.length > 0 && (
              <div className="card mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">What You Can Do</h3>
                <ActionSteps steps={result.steps} />
              </div>
            )}

            <div className="text-center py-6">
              <p className="text-gray-600 mb-4">Was this answer helpful?</p>
              <div className="space-x-4">
                <button className="btn-primary">Yes, helpful</button>
                <button className="btn-secondary">Not helpful</button>
              </div>
            </div>
          </>
        )}

        {!loading && !error && !result && query && (
          <div className="text-center py-12 text-gray-600">
            No results found for "{query}"
          </div>
        )}
      </div>
    </div>
  )
}
