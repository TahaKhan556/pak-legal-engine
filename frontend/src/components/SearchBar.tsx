import { Search } from 'lucide-react'
import { useState, FormEvent, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'

interface SearchBarProps {
  large?: boolean
  autoFocus?: boolean
}

export function SearchBar({ large = false, autoFocus = false }: SearchBarProps) {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus()
    }
  }, [autoFocus])

  useEffect(() => {
    if (query.length > 1) {
      api.get(`/api/v1/search/suggestions?q=${encodeURIComponent(query)}`)
        .then((res) => setSuggestions(res.data))
        .catch(() => setSuggestions([]))
    } else {
      setSuggestions([])
    }
  }, [query])

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      setShowSuggestions(false)
      navigate(`/search?q=${encodeURIComponent(query.trim())}`)
    }
  }

  const handleSuggestionClick = (s: string) => {
    setQuery(s)
    setShowSuggestions(false)
    navigate(`/search?q=${encodeURIComponent(s)}`)
  }

  return (
    <form onSubmit={handleSubmit} className="relative w-full max-w-2xl mx-auto">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => { setQuery(e.target.value); setShowSuggestions(true); }}
          onFocus={() => setShowSuggestions(true)}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          placeholder="Ask a legal question... e.g., Can police check my phone?"
          className={`w-full pl-12 pr-28 bg-white border border-gray-200 text-gray-900 placeholder:text-gray-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-kanun-500 focus:border-kanun-500 transition-all shadow-sm ${
            large ? 'py-4 text-lg' : 'py-3 text-base'
          }`}
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-kanun-700 text-white px-5 py-2 rounded-lg font-medium text-sm hover:bg-kanun-800 active:bg-kanun-900 transition-all focus:outline-none focus:ring-2 focus:ring-kanun-500 focus:ring-offset-2"
        >
          Search
        </button>
      </div>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-100 rounded-xl shadow-lg overflow-hidden z-50">
          {suggestions.map((s, i) => (
            <button
              key={i}
              type="button"
              onClick={() => handleSuggestionClick(s)}
              className="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-kanun-50 transition-colors flex items-center gap-3"
            >
              <Search className="h-4 w-4 text-gray-400 flex-shrink-0" />
              {s}
            </button>
          ))}
        </div>
      )}
    </form>
  )
}
