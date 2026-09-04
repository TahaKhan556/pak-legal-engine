import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { Results } from './pages/Results'
import { Browse } from './pages/Browse'
import { Contribute } from './pages/Contribute'
import { Admin } from './pages/Admin'
import { Header } from './components/Header'
import { Footer } from './components/Footer'

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Results />} />
            <Route path="/browse" element={<Browse />} />
            <Route path="/contribute" element={<Contribute />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
