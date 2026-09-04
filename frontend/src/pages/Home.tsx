import { SearchBar } from '../components/SearchBar'
import { Scale, Shield, BookOpen, Users, ChevronRight } from 'lucide-react'
import { Link } from 'react-router-dom'

const categories = [
  { icon: Scale, label: 'Constitution', description: 'Fundamental rights & directive principles', href: '/browse?search=constitution', color: 'bg-kanun-100 text-kanun-700' },
  { icon: Shield, label: 'Criminal Law', description: 'PPC, CrPC & criminal procedures', href: '/browse?search=criminal', color: 'bg-red-50 text-red-700' },
  { icon: BookOpen, label: 'Civil Law', description: 'Contracts, property & civil disputes', href: '/browse?search=civil', color: 'bg-blue-50 text-blue-700' },
  { icon: Users, label: 'Family Law', description: 'Marriage, divorce & custody', href: '/browse?search=family', color: 'bg-purple-50 text-purple-700' },
]

const popularQuestions = [
  "Can police check my phone without a warrant?",
  "How to file an FIR in Pakistan?",
  "What are my rights during arrest?",
  "Can anyone file an FIR without evidence?",
]

export function Home() {
  return (
    <div className="min-h-screen">
      <section className="relative overflow-hidden bg-gradient-to-b from-kanun-50 to-white">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMS41IiBmaWxsPSIjMTU4MDNkIiBmaWxsLW9wYWNpdHk9IjAuMDUiLz48L3N2Zz4=')]"></div>
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 pt-16 pb-20 md:pt-24 md:pb-28">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center gap-2 bg-kanun-100/80 text-kanun-700 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
              <Scale className="h-4 w-4" />
              Pakistani Legal Knowledge Engine
            </div>
            <h1 className="text-display text-gray-900 mb-4">
              Know Your Rights.
              <br />
              <span className="text-kanun-700">Instantly.</span>
            </h1>
            <p className="text-lg text-gray-500 mb-8 max-w-xl mx-auto leading-relaxed">
              Search Pakistani law in plain language. Get instant answers backed by constitutional articles, penal codes, and legal provisions.
            </p>
            <SearchBar large autoFocus />

            <div className="flex flex-wrap items-center justify-center gap-3 mt-6">
              <span className="text-xs text-gray-400">Try:</span>
              {popularQuestions.slice(0, 3).map((q, i) => (
                <Link
                  key={i}
                  to={`/search?q=${encodeURIComponent(q)}`}
                  className="text-xs text-kanun-600 hover:text-kanun-700 bg-kanun-50 hover:bg-kanun-100 px-3 py-1.5 rounded-full transition-colors"
                >
                  {q}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 sm:px-6 -mt-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.label}
              to={cat.href}
              className="card-hover group cursor-pointer"
            >
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${cat.color}`}>
                <cat.icon className="h-5 w-5" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-1">{cat.label}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{cat.description}</p>
              <div className="mt-3 flex items-center gap-1 text-sm font-medium text-kanun-600 group-hover:text-kanun-700">
                Browse <ChevronRight className="h-4 w-4 group-hover:translate-x-0.5 transition-transform" />
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-heading text-gray-900 mb-3">How It Works</h2>
          <p className="text-gray-500 max-w-lg mx-auto">Three steps to understanding your legal rights</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { step: '01', title: 'Ask Your Question', desc: 'Type your legal question in English or describe your situation naturally.' },
            { step: '02', title: 'Get Legal Answer', desc: 'AI searches 958+ federal laws and explains them in plain language.' },
            { step: '03', title: 'Know Your Rights', desc: 'Get actionable steps with exact legal references you can use.' },
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="text-5xl font-bold text-kanun-100 mb-4">{item.step}</div>
              <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-kanun-950 text-white py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { value: '958+', label: 'Laws Indexed' },
              { value: '4,100+', label: 'Legal Sections' },
              { value: '22', label: 'Law Categories' },
              { value: '24/7', label: 'Available' },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="text-3xl font-bold text-kanun-400 mb-1">{stat.value}</div>
                <div className="text-sm text-kanun-200/60">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
