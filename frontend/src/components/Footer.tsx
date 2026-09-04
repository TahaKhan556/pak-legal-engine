import { Scale } from 'lucide-react'

export function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <Scale className="h-6 w-6 text-primary-500" />
            <span className="text-white font-semibold">Kanun</span>
          </div>

          <p className="text-sm text-center md:text-right">
            Empowering citizens with legal knowledge. Not legal advice.
          </p>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-800 text-center text-sm">
          <p>
            Built for the people of Pakistan. Data sourced from official government portals.
          </p>
        </div>
      </div>
    </footer>
  )
}
