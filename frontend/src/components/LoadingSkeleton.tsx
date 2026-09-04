export function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="card">
        <div className="h-4 bg-gray-200 rounded w-24 mb-3"></div>
        <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-6 bg-gray-200 rounded w-1/2"></div>
      </div>
      <div className="card">
        <div className="h-4 bg-gray-200 rounded w-32 mb-3"></div>
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
      <div className="card">
        <div className="h-4 bg-gray-200 rounded w-28 mb-3"></div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-start gap-3">
              <div className="w-8 h-8 bg-gray-200 rounded-lg flex-shrink-0"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-2/3 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/3"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
