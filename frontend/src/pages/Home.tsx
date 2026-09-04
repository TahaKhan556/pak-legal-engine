import { SearchBar } from '../components/SearchBar'
import { CategoryButtons } from '../components/CategoryButtons'
import { Stats } from '../components/Stats'

export function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <main className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Kanun <span className="text-primary-600">قانون</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Your rights, explained simply. Ask any legal question about Pakistani law.
          </p>

          <SearchBar large />
        </div>

        <CategoryButtons />
        <Stats />

        <div className="mt-16 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-4">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-primary-600 font-bold text-xl">1</span>
              </div>
              <h3 className="font-semibold mb-2">Ask a Question</h3>
              <p className="text-sm text-gray-600">Type your legal question in English or describe your situation</p>
            </div>
            <div className="text-center p-4">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-primary-600 font-bold text-xl">2</span>
              </div>
              <h3 className="font-semibold mb-2">Get Legal Answer</h3>
              <p className="text-sm text-gray-600">AI-powered search finds relevant laws and explains them simply</p>
            </div>
            <div className="text-center p-4">
              <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-primary-600 font-bold text-xl">3</span>
              </div>
              <h3 className="font-semibold mb-2">Know Your Rights</h3>
              <p className="text-sm text-gray-600">Get step-by-step guidance with exact legal references</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
