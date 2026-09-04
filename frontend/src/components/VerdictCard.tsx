import { CheckCircle, XCircle } from 'lucide-react'

interface VerdictCardProps {
  verdict: string
}

export function VerdictCard({ verdict }: VerdictCardProps) {
  const isYes = verdict.toUpperCase().startsWith('YES')

  return (
    <div className={`card border-l-4 ${
      isYes ? 'border-l-kanun-500 bg-kanun-50/30' : 'border-l-red-500 bg-red-50/30'
    }`}>
      <div className="flex items-start gap-4">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
          isYes ? 'bg-kanun-100' : 'bg-red-100'
        }`}>
          {isYes
            ? <CheckCircle className="h-5 w-5 text-kanun-600" />
            : <XCircle className="h-5 w-5 text-red-600" />
          }
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">The Verdict</h3>
          <p className="text-lg font-semibold text-gray-900 leading-relaxed">{verdict}</p>
        </div>
      </div>
    </div>
  )
}
