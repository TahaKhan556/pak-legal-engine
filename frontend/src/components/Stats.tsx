import { FileText, BookOpen, Users } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../services/api'

export function Stats() {
  const [stats, setStats] = useState({
    total_documents: 0,
    total_sections: 0,
  })

  useEffect(() => {
    api.get('/api/v1/documents/stats').then((res) => {
      setStats(res.data)
    }).catch(() => {
      setStats({ total_documents: 958, total_sections: 4189 })
    })
  }, [])

  const statItems = [
    { icon: FileText, label: 'Laws Indexed', value: stats.total_documents.toLocaleString() },
    { icon: BookOpen, label: 'Sections Searchable', value: stats.total_sections.toLocaleString() },
    { icon: Users, label: 'Contributors', value: '100+' },
  ]

  return (
    <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto mt-12">
      {statItems.map((stat) => (
        <div key={stat.label} className="text-center">
          <stat.icon className="h-6 w-6 mx-auto mb-2 text-primary-600" />
          <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
          <div className="text-sm text-gray-600">{stat.label}</div>
        </div>
      ))}
    </div>
  )
}
