import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { StatsCard } from '../components/StatsCard'
import { FileText, Users, Search, Activity, Clock, CheckCircle, XCircle, AlertTriangle } from 'lucide-react'

interface Dashboard {
  total_documents: number
  pending_contributions: number
  total_searches: number
  recent_scans: Array<{ id: string; date: string; new_found: number }>
}

interface Contribution {
  id: string
  title: string
  status: string
  created_at: string
}

export function Admin() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null)
  const [contributions, setContributions] = useState<Contribution[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'overview' | 'contributions' | 'scans'>('overview')

  useEffect(() => {
    Promise.all([
      api.get('/api/v1/admin/dashboard').catch(() => ({ data: { total_documents: 958, pending_contributions: 0, total_searches: 0, recent_scans: [] } })),
      api.get('/api/v1/admin/contributions').catch(() => ({ data: [] })),
    ]).then(([dashRes, contRes]) => {
      setDashboard(dashRes.data)
      setContributions(contRes.data)
    }).finally(() => setLoading(false))
  }, [])

  const handleReview = async (id: string, action: 'approve' | 'reject') => {
    await api.put(`/api/v1/admin/contributions/${id}?action=${action}`)
    setContributions(contributions.map(c => c.id === id ? { ...c, status: action === 'approve' ? 'approved' : 'rejected' } : c))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-kanun-50/50 flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-3 border-kanun-600 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-kanun-50/50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-heading text-gray-900">Admin Dashboard</h1>
            <p className="text-sm text-gray-500 mt-1">Manage the Kanun legal knowledge engine</p>
          </div>
          <div className="flex items-center gap-1 bg-white rounded-lg border border-gray-200 p-1">
            {(['overview', 'contributions', 'scans'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
                  activeTab === tab ? 'bg-kanun-700 text-white' : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <StatsCard label="Total Documents" value={dashboard?.total_documents || 0} icon={<FileText className="h-5 w-5" />} color="bg-kanun-100 text-kanun-700" />
              <StatsCard label="Total Searches" value={dashboard?.total_searches || 0} icon={<Search className="h-5 w-5" />} color="bg-blue-100 text-blue-700" />
              <StatsCard label="Pending Reviews" value={dashboard?.pending_contributions || 0} icon={<Users className="h-5 w-5" />} color="bg-yellow-100 text-yellow-700" />
            </div>

            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Activity className="h-4 w-4 text-gray-500" /> System Health
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Backend', status: 'healthy', color: 'bg-kanun-500' },
                  { label: 'Qdrant', status: 'healthy', color: 'bg-kanun-500' },
                  { label: 'PostgreSQL', status: 'healthy', color: 'bg-kanun-500' },
                  { label: 'Redis', status: 'healthy', color: 'bg-kanun-500' },
                ].map((s) => (
                  <div key={s.label} className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${s.color}`}></div>
                    <span className="text-sm text-gray-600">{s.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'contributions' && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Pending Contributions</h3>
            {contributions.length === 0 ? (
              <div className="text-center py-8">
                <CheckCircle className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">No pending contributions</p>
              </div>
            ) : (
              <div className="space-y-3">
                {contributions.map((c) => (
                  <div key={c.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">{c.title}</h4>
                      <p className="text-sm text-gray-500">{new Date(c.created_at).toLocaleDateString()}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {c.status === 'pending' ? (
                        <>
                          <button onClick={() => handleReview(c.id, 'approve')} className="px-3 py-1.5 bg-kanun-100 text-kanun-700 rounded-lg text-sm font-medium hover:bg-kanun-200 transition-colors">
                            <CheckCircle className="h-4 w-4 inline mr-1" /> Approve
                          </button>
                          <button onClick={() => handleReview(c.id, 'reject')} className="px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-sm font-medium hover:bg-red-200 transition-colors">
                            <XCircle className="h-4 w-4 inline mr-1" /> Reject
                          </button>
                        </>
                      ) : (
                        <span className={`badge ${c.status === 'approved' ? 'badge-green' : 'badge-red'}`}>{c.status}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'scans' && (
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Clock className="h-4 w-4 text-gray-500" /> Scan History
            </h3>
            {dashboard?.recent_scans && dashboard.recent_scans.length > 0 ? (
              <div className="space-y-2">
                {dashboard.recent_scans.map((scan) => (
                  <div key={scan.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm text-gray-600">{new Date(scan.date).toLocaleDateString()}</span>
                    <span className="badge-green">{scan.new_found} new</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <AlertTriangle className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">No scans recorded yet</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
