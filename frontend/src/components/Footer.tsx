import { Scale } from 'lucide-react'

export function Footer() {
  return (
    <footer className="bg-kanun-950 text-white mt-auto">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-8 h-8 bg-kanun-600 rounded-lg flex items-center justify-center">
                <Scale className="h-4 w-4 text-white" />
              </div>
              <span className="text-lg font-bold">Kanun</span>
            </div>
            <p className="text-sm text-kanun-200/60 leading-relaxed max-w-xs">
              Empowering citizens with accessible legal knowledge. Your rights, explained simply.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-sm uppercase tracking-wider text-kanun-200/80">Legal Resources</h4>
            <ul className="space-y-2 text-sm text-kanun-200/60">
              <li>Constitution of Pakistan</li>
              <li>Pakistan Penal Code</li>
              <li>Code of Criminal Procedure</li>
              <li>PECA 2016</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-sm uppercase tracking-wider text-kanun-200/80">Data Sources</h4>
            <ul className="space-y-2 text-sm text-kanun-200/60">
              <li>Pakistan Code (pakistancode.gov.pk)</li>
              <li>KP Code (kpcode.kp.gov.pk)</li>
              <li>Sindh Assembly (pas.gov.pk)</li>
              <li>National Assembly (na.gov.pk)</li>
            </ul>
          </div>
        </div>
        <div className="mt-10 pt-6 border-t border-kanun-800/50 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-xs text-kanun-200/40">
            Not legal advice. Always consult a qualified lawyer.
          </p>
          <p className="text-xs text-kanun-200/40">
            Built for the people of Pakistan
          </p>
        </div>
      </div>
    </footer>
  )
}
