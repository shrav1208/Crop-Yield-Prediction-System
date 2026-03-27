import { useState } from 'react'
import './Page.css'
import './YieldPage.css'

const CROPS = [
  'coffee', 'cotton', 'groundnut', 'jute', 'maize',
  'onion', 'potato', 'rice', 'rubber', 'soybean',
  'sugarcane', 'sunflower', 'tea', 'tomato', 'wheat'
]

export default function YieldPage() {
  const [fields, setFields] = useState({
    crop: '', soil_temp: '', nitrogen: '', phosphorus: '',
    potassium: '', moisture: '', humidity: '', air_temp: ''
  })
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')

  const set = (k) => (e) => setFields(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true); setError(''); setResult(null)
    try {
      const res  = await fetch('http://127.0.0.1:5000/yield', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          crop:       fields.crop,
          soil_temp:  Number(fields.soil_temp),
          nitrogen:   Number(fields.nitrogen),
          phosphorus: Number(fields.phosphorus),
          potassium:  Number(fields.potassium),
          moisture:   Number(fields.moisture),
          humidity:   Number(fields.humidity),
          air_temp:   Number(fields.air_temp),
        }),
      })
      const data = await res.json()
      if (data.error) { setError(data.error); return }
      setResult(data)
    } catch {
      setError('Could not reach the server. Is Flask running?')
    } finally {
      setLoading(false)
    }
  }



  return (
    <div className="page-wrapper">
      <div className="card">
        <div className="card-header">
          <span className="card-icon">📊</span>
          <h1 className="card-title">Yield Prediction</h1>
          <p className="card-subtitle">Enter crop and field conditions to estimate harvest yield.</p>
        </div>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-grid">
            <label className="field field--full">
              <span className="field-label">Crop</span>
              <select className="field-input" value={fields.crop} onChange={set('crop')} required>
                <option value="" disabled>Select a crop…</option>
                {CROPS.map(c => (
                  <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                ))}
              </select>
            </label>

            <label className="field">
              <span className="field-label">Soil Temp (°C)</span>
              <input className="field-input" type="number" step="0.1" placeholder="e.g. 28" value={fields.soil_temp} onChange={set('soil_temp')} required />
            </label>
            <label className="field">
              <span className="field-label">Air Temp (°C)</span>
              <input className="field-input" type="number" step="0.1" placeholder="e.g. 25" value={fields.air_temp} onChange={set('air_temp')} required />
            </label>
            <label className="field">
              <span className="field-label">Nitrogen (N)</span>
              <input className="field-input" type="number" placeholder="e.g. 90" value={fields.nitrogen} onChange={set('nitrogen')} required />
            </label>
            <label className="field">
              <span className="field-label">Phosphorus (P)</span>
              <input className="field-input" type="number" placeholder="e.g. 50" value={fields.phosphorus} onChange={set('phosphorus')} required />
            </label>
            <label className="field">
              <span className="field-label">Potassium (K)</span>
              <input className="field-input" type="number" placeholder="e.g. 100" value={fields.potassium} onChange={set('potassium')} required />
            </label>
            <label className="field">
              <span className="field-label">Moisture (%)</span>
              <input className="field-input" type="number" step="0.1" placeholder="e.g. 70" value={fields.moisture} onChange={set('moisture')} required />
            </label>
            <label className="field">
              <span className="field-label">Humidity (%)</span>
              <input className="field-input" type="number" step="0.1" placeholder="e.g. 80" value={fields.humidity} onChange={set('humidity')} required />
            </label>
          </div>

          <button className="submit-btn" type="submit" disabled={loading}>
            {loading ? <span className="spinner" /> : 'Predict Yield'}
          </button>
        </form>

        {error && <div className="result-box result-box--error">{error}</div>}

        {result && (
          <div className="result-box result-box--success yield-result">
            <div className="yield-numeric">
              <span className="result-label">Estimated Yield</span>
              <span className="yield-value">
                {result.yield_kg_ha.toLocaleString()}
                <span className="yield-unit"> kg / ha</span>
              </span>
            </div>
            <div className="yield-divider" />
            <div className="yield-category">
              <span className="result-label">Category</span>
              <span className={`yield-badge yield-badge--${result.yield_category.toLowerCase()}`}>
                {result.yield_category}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}