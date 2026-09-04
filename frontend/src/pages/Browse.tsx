import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../services/api'
import { FileText, Filter } from 'lucide-react'

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

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-8">
          <aside className="w-full md:w-64 flex-shrink-0">
            <div className="card">
              <h3 className="font-semibold mb-4 flex items-center">
                <Filter className="h-4 w-4 mr-2" /> Filters
              </h3>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Document Type</label>
                  <select
                    className="input-field"
                    value={docType}
                    onChange={(e) => setSearchParams({ ...Object.fromEntries(searchParams), doc_type: e.target.value })}
                  >
                    <option value="">All Types</option>
                    <option value="constitution">Constitution</option>
                    <option value="ppc">Penal Code</option>
                    <option value="crpc">Criminal Procedure</option>
                    <option value="federal_act">Federal Acts</option>
                    <option value="provincial_act">Provincial Acts</option>
                    <option value="ordinance">Ordinances</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Province</label>
                  <select
                    className="input-field"
                    value={province}
                    onChange={(e) => setSearchParams({ ...Object.fromEntries(searchParams), province: e.target.value })}
                  >
                    <option value="">All Provinces</option>
                    <option value="federal">Federal</option>
                    <option value="sindh">Sindh</option>
                    <option value="punjab">Punjab</option>
                    <option value="kpk">KPK</option>
                    <option value="balochistan">Balochistan</option>
                  </select>
                </div>
              </div>
            </div>
          </aside>

          <main className="flex-1">
            <h1 className="text-2xl font-bold mb-6">Browse Laws</h1>

            {loading ? (
              <div className="text-center py-12">Loading...</div>
            ) : documents.length === 0 ? (
              <div className="text-center py-12 text-gray-600">
                No documents found. Try adjusting your filters.
              </div>
            ) : (
              <div className="space-y-4">
                {documents.map((doc) => (
                  <div key={doc.id} className="card hover:shadow-xl transition-shadow cursor-pointer">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <FileText className="h-5 w-5 text-primary-600" />
                          <h3 className="font-semibold text-lg">{doc.title}</h3>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-2">
                          <span className="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full">
                            {doc.document_type}
                          </span>
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                            {doc.province}
                          </span>
                          {doc.year && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                              {doc.year}
                            </span>
                          )}
                        </div>
                        {doc.description && (
                          <p className="text-sm text-gray-600 line-clamp-2">{doc.description}</p>
                        )}
                      </div>
                      <div className="text-sm text-gray-500 ml-4">
                        {doc.total_sections} sections
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="flex justify-center gap-2 mt-8">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="btn-secondary disabled:opacity-50"
              >
                Previous
              </button>
              <span className="py-2 px-4">Page {page}</span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={documents.length < 20}
                className="btn-secondary disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
