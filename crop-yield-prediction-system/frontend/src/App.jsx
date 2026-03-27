import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import CropPage       from './pages/CropPage'
import FertilizerPage from './pages/FertilizerPage'
import DiseasePage    from './pages/DiseasePage'
import YieldPage      from './pages/YieldPage'
import './App.css'

function App() {
  return (
    <>
      <Navbar />
      <main className="page-content">
        <Routes>
          <Route path="/"           element={<YieldPage />} />
          <Route path="/fertilizer" element={<FertilizerPage />} />
          <Route path="/disease"    element={<DiseasePage />} />
          <Route path="/crop"      element={<CropPage />} />
        </Routes>
      </main>
    </>
  )
}

export default App