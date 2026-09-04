interface StatsCardProps {
  label: string
  value: string | number
  icon: React.ReactNode
  color?: string
}

export function StatsCard({ label, value, icon, color = 'bg-kanun-100 text-kanun-700' }: StatsCardProps) {
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{typeof value === 'number' ? value.toLocaleString() : value}</p>
        </div>
        <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${color}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}
