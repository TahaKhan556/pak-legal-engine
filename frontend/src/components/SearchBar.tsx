import { Search } from 'lucide-react'
import { useState, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'

interface SearchBarProps {
  large?: boolean
}

export function SearchBar({ large = false }: SearchBarProps) {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query.trim())}`)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a legal question... e.g., Can police check my phone?"
          className={`w-full pl-12 pr-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all ${
            large ? 'py-5 text-lg' : 'py-3'
          }`}
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          Search
        </button>
      </div>
    </form>
  )
}
