import { Scale, FileText, Shield, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

const categories = [
  { icon: Scale, label: 'Constitution', query: 'constitution', color: 'bg-blue-100 text-blue-700' },
  { icon: FileText, label: 'Penal Code', query: 'penal code', color: 'bg-red-100 text-red-700' },
  { icon: Shield, label: 'Criminal Law', query: 'criminal', color: 'bg-orange-100 text-orange-700' },
  { icon: Users, label: 'Family Law', query: 'family', color: 'bg-purple-100 text-purple-700' },
]

export function CategoryButtons() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
      {categories.map((cat) => (
        <Link
          key={cat.label}
          to={`/browse?search=${cat.query}`}
          className={`flex flex-col items-center p-4 rounded-xl hover:scale-105 transition-transform ${cat.color}`}
        >
          <cat.icon className="h-8 w-8 mb-2" />
          <span className="font-medium text-sm">{cat.label}</span>
        </Link>
      ))}
    </div>
  )
}
