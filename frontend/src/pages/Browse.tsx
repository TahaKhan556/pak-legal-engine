import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../services/api'
import { FileText, Filter, ChevronLeft, ChevronRight } from 'lucide-react'

interface Document {
  id: string
  title: string
  document_type: string
  province: string
  year: number | null
  description: string | null
  total_sections: number
  source_url: string | null
  created_at: string
}

const docTypes = [
  { value: '', label: 'All Types' },
  { value: 'constitution', label: 'Constitution' },
  { value: 'ppc', label: 'Penal Code' },
  { value: 'crpc', label: 'Criminal Procedure' },
  { value: 'cpc', label: 'Civil Procedure' },
  { value: 'federal_act', label: 'Federal Acts' },
  { value: 'provincial_act', label: 'Provincial Acts' },
  { value: 'ordinance', label: 'Ordinances' },
]

const provinces = [
  { value: '', label: 'All Provinces' },
  { value: 'federal', label: 'Federal' },
  { value: 'sindh', label: 'Sindh' },
  { value: 'punjab', label: 'Punjab' },
  { value: 'kpk', label: 'KPK' },
  { value: 'balochistan', label: 'Balochistan' },
]

export function Browse() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)

  const docType = searchParams.get('doc_type') || ''
  const province = searchParams.get('province') || ''
  const search = searchParams.get('search') || ''

  useEffect(() => {
    setLoading(true)
    const params = new URLSearchParams()
    if (docType) params.set('doc_type', docType)
    if (province) params.set('province', province)
    if (search) params.set('search', search)
    params.set('page', String(page))

    api.get(`/api/v1/documents?${params}`)
      .then((res) => setDocuments(res.data))
      .catch(() => setDocuments([]))
      .finally(() => setLoading(false))
  }, [docType, province, search, page])

  const updateFilter = (key: string, value: string) => {
    const params = Object.fromEntries(searchParams)
    if (value) {
      params[key] = value
    } else {
      delete params[key]
    }
    setSearchParams(params)
    setPage(1)
  }

  return (
    <div className="min-h-screen bg-kanun-50/50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          <aside className="w-full lg:w-64 flex-shrink-0">
            <div className="card sticky top-24">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Filter className="h-4 w-4 text-gray-500" /> Filters
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wider">Document Type</label>
                  <select
                    className="input-field text-sm"
                    value={docType}
                    onChange={(e) => updateFilter('doc_type', e.target.value)}
                  >
                    {docTypes.map((dt) => (
                      <option key={dt.value} value={dt.value}>{dt.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wider">Province</label>
                  <select
                    className="input-field text-sm"
                    value={province}
                    onChange={(e) => updateFilter('province', e.target.value)}
                  >
                    {provinces.map((p) => (
                      <option key={p.value} value={p.value}>{p.label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </aside>

          <main className="flex-1">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-heading text-gray-900">Browse Laws</h1>
              <span className="text-sm text-gray-500">{documents.length} results</span>
            </div>

            {loading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="card animate-pulse">
                    <div className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-gray-200 rounded-lg"></div>
                      <div className="flex-1">
                        <div className="h-5 bg-gray-200 rounded w-2/3 mb-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-1/3"></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : documents.length === 0 ? (
              <div className="card text-center py-12">
                <FileText className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">No documents found matching your filters.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {documents.map((doc) => (
                  <div key={doc.id} className="card-hover cursor-pointer">
                    <div className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-kanun-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <FileText className="h-5 w-5 text-kanun-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 leading-snug mb-1">{doc.title}</h3>
                        <div className="flex flex-wrap gap-1.5">
                          <span className="badge-green text-[11px]">{doc.document_type}</span>
                          <span className="badge-blue text-[11px]">{doc.province}</span>
                          {doc.year && <span className="badge-gray text-[11px]">{doc.year}</span>}
                          <span className="badge-gray text-[11px]">{doc.total_sections} sections</span>
                        </div>
                        {doc.description && (
                          <p className="text-sm text-gray-500 mt-2 line-clamp-2">{doc.description}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="flex items-center justify-center gap-2 mt-8">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="btn-secondary disabled:opacity-40 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              <span className="px-4 py-2 text-sm text-gray-600">Page {page}</span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={documents.length < 20}
                className="btn-secondary disabled:opacity-40 disabled:cursor-not-allowed"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
