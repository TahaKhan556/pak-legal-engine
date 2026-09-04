import { useSearchParams, Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { SearchBar } from '../components/SearchBar'
import { VerdictCard } from '../components/VerdictCard'
import { LegalCard } from '../components/LegalCard'
import { LoadingSkeleton } from '../components/LoadingSkeleton'
import { EmptyState } from '../components/EmptyState'
import { CheckCircle, ArrowLeft, Share2 } from 'lucide-react'

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
  const [feedback, setFeedback] = useState<'helpful' | 'not_helpful' | null>(null)

  useEffect(() => {
    if (query) {
      setLoading(true)
      setError('')
      setResult(null)
      api.post('/api/v1/search', { query })
        .then((res) => setResult(res.data))
        .catch((err) => setError(err.response?.data?.detail || 'Failed to search. Please try again.'))
        .finally(() => setLoading(false))
    }
  }, [query])

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
  }

  return (
    <div className="min-h-screen bg-kanun-50/50">
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-5">
          <div className="flex items-center gap-3 mb-4">
            <Link to="/" className="text-gray-400 hover:text-gray-600 transition-colors">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <span className="text-sm text-gray-400">Search Results</span>
          </div>
          <SearchBar />
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
        {loading && <LoadingSkeleton />}

        {error && <EmptyState type="error" message={error} />}

        {!loading && !error && !result && query && (
          <EmptyState type="no-results" query={query} />
        )}

        {result && (
          <div className="space-y-6">
            <VerdictCard verdict={result.verdict} />

            <div className="card">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Plain Language Explanation</h3>
              <div className="text-gray-700 leading-relaxed whitespace-pre-line">{result.plain_language}</div>
            </div>

            {result.plain_urdu && (
              <div className="card border-r-4 border-kanun-500 bg-kanun-50/30">
                <h3 className="text-sm font-semibold text-kanun-600 uppercase tracking-wider mb-3">Roman Urdu</h3>
                <p className="text-gray-700 leading-relaxed whitespace-pre-line text-right" dir="rtl">{result.plain_urdu}</p>
              </div>
            )}

            {result.steps.length > 0 && (
              <div className="card">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">What You Can Do</h3>
                <ol className="space-y-3">
                  {result.steps.map((step, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <div className="w-6 h-6 bg-kanun-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs font-bold text-kanun-700">{i + 1}</span>
                      </div>
                      <span className="text-gray-700 leading-relaxed">{step}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {result.legal_references.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Legal References</h3>
                <div className="space-y-3">
                  {result.legal_references.map((ref, i) => (
                    <LegalCard key={ref.id} reference={ref} index={i} />
                  ))}
                </div>
              </div>
            )}

            <div className="card">
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                  <p className="text-sm text-gray-500 mb-2">Was this answer helpful?</p>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setFeedback('helpful')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        feedback === 'helpful'
                          ? 'bg-kanun-100 text-kanun-700'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      <CheckCircle className="h-4 w-4 inline mr-1.5" />
                      Yes
                    </button>
                    <button
                      onClick={() => setFeedback('not_helpful')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        feedback === 'not_helpful'
                          ? 'bg-red-100 text-red-700'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      No
                    </button>
                  </div>
                </div>
                <button
                  onClick={handleShare}
                  className="btn-ghost text-sm"
                >
                  <Share2 className="h-4 w-4" />
                  Copy link
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
