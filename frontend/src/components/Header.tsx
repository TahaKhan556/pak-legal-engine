import { Link, useLocation } from 'react-router-dom'
import { Scale, Menu, X } from 'lucide-react'
import { useState } from 'react'

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()

  const links = [
    { path: '/', label: 'Search' },
    { path: '/browse', label: 'Browse Laws' },
    { path: '/contribute', label: 'Contribute' },
    { path: '/admin', label: 'Admin' },
  ]

  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b border-kanun-100/50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 bg-kanun-700 rounded-lg flex items-center justify-center group-hover:bg-kanun-800 transition-colors">
              <Scale className="h-5 w-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold text-gray-900 leading-tight tracking-tight">Kanun</span>
              <span className="text-[10px] font-medium text-kanun-600 leading-tight tracking-wider uppercase">قانون</span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {links.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                  location.pathname === link.path
                    ? 'bg-kanun-50 text-kanun-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          <button
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>

        {mobileOpen && (
          <nav className="md:hidden py-3 border-t border-gray-100">
            {links.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`block px-3 py-2.5 rounded-lg text-sm font-medium ${
                  location.pathname === link.path
                    ? 'bg-kanun-50 text-kanun-700'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
                onClick={() => setMobileOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        )}
      </div>
    </header>
  )
}
