import { SearchX, AlertTriangle, FileQuestion } from 'lucide-react'

interface EmptyStateProps {
  type: 'no-results' | 'error' | 'no-data'
  query?: string
  message?: string
}

export function EmptyState({ type, query, message }: EmptyStateProps) {
  const configs = {
    'no-results': {
      icon: SearchX,
      title: 'No relevant results found',
      description: query
        ? `No legal provisions matching "${query}" were found in the database. Try rephrasing your question or use different keywords.`
        : 'No results found. Try a different search query.',
      color: 'text-gray-400',
      bg: 'bg-gray-100',
    },
    'error': {
      icon: AlertTriangle,
      title: 'Something went wrong',
      description: message || 'An error occurred while processing your request. Please try again.',
      color: 'text-red-400',
      bg: 'bg-red-50',
    },
    'no-data': {
      icon: FileQuestion,
      title: 'No data available',
      description: 'The legal database is being populated. Please check back later.',
      color: 'text-kanun-400',
      bg: 'bg-kanun-50',
    },
  }

  const config = configs[type]
  const Icon = config.icon

  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className={`w-16 h-16 ${config.bg} rounded-2xl flex items-center justify-center mb-4`}>
        <Icon className={`h-8 w-8 ${config.color}`} />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{config.title}</h3>
      <p className="text-sm text-gray-500 max-w-md">{config.description}</p>
    </div>
  )
}
