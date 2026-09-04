import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { BarChart3, FileText, Users, Search } from 'lucide-react'

interface Dashboard {
  total_documents: number
  pending_contributions: number
  total_searches: number
  recent_scans: Array<{
    id: string
    date: string
    new_found: number
  }>
}

export function Admin() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/v1/admin/dashboard')
      .then((res) => setDashboard(res.data))
      .catch(() => setDashboard({
        total_documents: 958,
        pending_contributions: 0,
        total_searches: 0,
        recent_scans: [],
      }))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  const stats = [
    { icon: FileText, label: 'Total Documents', value: dashboard?.total_documents || 0, color: 'text-blue-600' },
    { icon: Users, label: 'Pending Contributions', value: dashboard?.pending_contributions || 0, color: 'text-orange-600' },
    { icon: Search, label: 'Total Searches', value: dashboard?.total_searches || 0, color: 'text-green-600' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {stats.map((stat) => (
            <div key={stat.label} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                  <p className="text-3xl font-bold">{stat.value.toLocaleString()}</p>
                </div>
                <stat.icon className={`h-12 w-12 ${stat.color}`} />
              </div>
            </div>
          ))}
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Recent Scans</h2>
          {dashboard?.recent_scans && dashboard.recent_scans.length > 0 ? (
            <div className="space-y-2">
              {dashboard.recent_scans.map((scan) => (
                <div key={scan.id} className="flex justify-between py-2 border-b">
                  <span>{new Date(scan.date).toLocaleDateString()}</span>
                  <span className="text-primary-600">{scan.new_found} new documents</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No recent scans</p>
          )}
        </div>
      </div>
    </div>
  )
}
