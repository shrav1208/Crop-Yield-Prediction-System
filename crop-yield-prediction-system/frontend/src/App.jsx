import { useState } from "react";
import "./App.css";

function App() {
  const [temperature, setTemperature] = useState("");
  const [rainfall, setRainfall] = useState("");
  const [soilType, setSoilType] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        temperature: Number(temperature),
        rainfall: Number(rainfall),
        soilType,
      }),
    });

    const data = await response.json();
    setResult(data.recommended_crop);
  };

  return (
    <div className="container">
      <h1>AIML Powered Yield Prediction System 🌾</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Temperature (°C)"
          value={temperature}
          onChange={(e) => setTemperature(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Rainfall (mm)"
          value={rainfall}
          onChange={(e) => setRainfall(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Soil Type"
          value={soilType}
          onChange={(e) => setSoilType(e.target.value)}
          required
        />

        <button type="submit">Predict Crop</button>
      </form>

      {result && (
        <div className="result">
          🌱 Recommended Crop: <strong>{result}</strong>
        </div>
      )}
    </div>
  );
}

export default App;
