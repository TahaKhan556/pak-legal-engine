import { FileText, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'

interface LegalCardProps {
  reference: {
    id: string
    title: string
    section: string
    content: string
    score: number
    doc_type: string
    year: number | null
    source_url: string
  }
  index: number
}

export function LegalCard({ reference, index }: LegalCardProps) {
  const [expanded, setExpanded] = useState(false)
  const scorePercent = Math.round(reference.score * 100)

  return (
    <div className="card-hover">
      <div className="flex items-start gap-4">
        <div className="w-8 h-8 bg-kanun-100 rounded-lg flex items-center justify-center flex-shrink-0">
          <span className="text-sm font-bold text-kanun-700">{index + 1}</span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h4 className="font-semibold text-gray-900 leading-snug">{reference.title}</h4>
              <p className="text-sm text-gray-500 mt-0.5">{reference.section}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                scorePercent >= 80 ? 'bg-kanun-100 text-kanun-700' :
                scorePercent >= 65 ? 'bg-yellow-100 text-yellow-700' :
                'bg-gray-100 text-gray-600'
              }`}>
                {scorePercent}% match
              </span>
              {reference.source_url && (
                <a
                  href={reference.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-kanun-600 transition-colors"
                >
                  <ExternalLink className="h-4 w-4" />
                </a>
              )}
            </div>
          </div>

          <div className="flex flex-wrap gap-1.5 mt-2">
            <span className="badge-green text-[11px]">{reference.doc_type}</span>
            {reference.year && (
              <span className="badge-gray text-[11px]">{reference.year}</span>
            )}
          </div>

          <button
            onClick={() => setExpanded(!expanded)}
            className="mt-3 flex items-center gap-1 text-sm text-kanun-600 hover:text-kanun-700 font-medium transition-colors"
          >
            {expanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            {expanded ? 'Show less' : 'Show full text'}
          </button>

          {expanded && (
            <div className="mt-3 p-4 bg-gray-50 rounded-lg text-sm text-gray-700 leading-relaxed max-h-64 overflow-y-auto">
              {reference.content}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
