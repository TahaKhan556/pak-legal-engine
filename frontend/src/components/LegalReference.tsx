import { FileText, ExternalLink } from 'lucide-react'

interface LegalReferenceProps {
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
}

export function LegalReference({ reference }: LegalReferenceProps) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary-600" />
          <div>
            <h4 className="font-semibold">{reference.title}</h4>
            <p className="text-sm text-gray-600">{reference.section}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">
            {Math.round(reference.score * 100)}% match
          </span>
          {reference.source_url && (
            <a
              href={reference.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700"
            >
              <ExternalLink className="h-4 w-4" />
            </a>
          )}
        </div>
      </div>
      <p className="mt-2 text-sm text-gray-700 line-clamp-3">{reference.content}</p>
      <div className="mt-2 flex gap-2">
        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
          {reference.doc_type}
        </span>
        {reference.year && (
          <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
            {reference.year}
          </span>
        )}
      </div>
    </div>
  )
}
