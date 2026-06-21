import { useState } from "react"
import axios from "axios"

const biasMap = {
  FOMO: { label: "Social Proof / Herd Behaviour", icon: "👥", color: "text-orange-400" },
  LOSS: { label: "Loss Aversion", icon: "📉", color: "text-red-400" },
  ANCHOR: { label: "Anchoring Bias", icon: "⚓", color: "text-yellow-400" },
  SCARCITY: { label: "Scarcity Heuristic", icon: "⏰", color: "text-orange-500" },
  GAMIFY: { label: "Variable Reward Loop", icon: "🎮", color: "text-purple-400" },
  DEFAULT: { label: "Default Bias", icon: "🔘", color: "text-blue-400" },
  CLEAN: { label: "No manipulation detected", icon: "✅", color: "text-green-400" },
}

export default function Analyser() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = (e) => {
    const f = e.target.files[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
  }

  const handleAnalyse = async () => {
    if (!file) return
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append("file", file)
      const res = await axios.post("/api/analyse", formData)
      setResult(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const scoreColor = (score) => {
    if (score > 60) return "text-red-400"
    if (score > 30) return "text-yellow-400"
    return "text-green-400"
  }

  const scoreEmoji = (score) => {
    if (score > 60) return "🔴"
    if (score > 30) return "🟡"
    return "🟢"
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {/* Left — Upload */}
      <div>
        <h2 className="text-lg font-semibold mb-4 text-gray-200">Upload Screenshot</h2>
        <label className="block border-2 border-dashed border-gray-700 rounded-xl p-8 text-center cursor-pointer hover:border-blue-500 transition-colors">
          <input type="file" accept=".png,.jpg,.jpeg" onChange={handleUpload} className="hidden" />
          {preview ? (
            <img src={preview} alt="preview" className="max-h-80 mx-auto rounded-lg" />
          ) : (
            <div className="text-gray-500">
              <p className="text-4xl mb-3">📱</p>
              <p className="text-sm">Click to upload a fintech app screenshot</p>
              <p className="text-xs mt-1">PNG, JPG supported</p>
            </div>
          )}
        </label>

        {file && (
          <button
            onClick={handleAnalyse}
            disabled={loading}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-900 text-white font-medium py-3 rounded-lg transition-colors"
          >
            {loading ? "Analysing..." : "Analyse Screenshot"}
          </button>
        )}
      </div>

      {/* Right — Results */}
      <div>
        <h2 className="text-lg font-semibold mb-4 text-gray-200">Analysis Result</h2>

        {!result && !loading && (
          <div className="border border-gray-800 rounded-xl p-8 text-center text-gray-600">
            <p className="text-4xl mb-3">🔍</p>
            <p className="text-sm">Upload and analyse a screenshot to see results</p>
          </div>
        )}

        {loading && (
          <div className="border border-gray-800 rounded-xl p-8 text-center text-gray-400">
            <p className="text-4xl mb-3 animate-pulse">⚙️</p>
            <p className="text-sm">Running CLIP + OCR analysis...</p>
          </div>
        )}

        {result && (
          <div className="space-y-4">
            {/* Metrics */}
            <div className="grid grid-cols-3 gap-3">
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">Pattern</p>
                <p className="text-lg font-bold text-white">
                  {biasMap[result.pattern]?.icon} {result.pattern}
                </p>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">NudgeScore</p>
                <p className={`text-lg font-bold ${scoreColor(result.nudge_score)}`}>
                  {scoreEmoji(result.nudge_score)} {result.nudge_score}/100
                </p>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">Confidence</p>
                <p className="text-lg font-bold text-white">{result.confidence}%</p>
              </div>
            </div>

            {/* Bias */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
              <p className="text-xs text-gray-500 mb-1">Bias Exploited</p>
              <p className={`font-medium ${biasMap[result.pattern]?.color}`}>
                {biasMap[result.pattern]?.label}
              </p>
            </div>

            {/* Finance impact */}
            {result.pattern !== "CLEAN" && (
              <div className="bg-red-950 border border-red-900 rounded-xl p-4">
                <p className="text-xs text-red-400 mb-2 font-medium">⚠️ Estimated 10-Year Financial Impact</p>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div>
                    <p className="text-xs text-gray-500">Without nudges</p>
                    <p className="text-sm font-bold text-green-400">₹{result.finance.clean.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">With nudges</p>
                    <p className="text-sm font-bold text-red-400">₹{result.finance.nudged.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Hidden cost</p>
                    <p className="text-sm font-bold text-red-300">₹{result.finance.loss.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            )}

            {result.pattern === "CLEAN" && (
              <div className="bg-green-950 border border-green-900 rounded-xl p-4">
                <p className="text-green-400 font-medium">✅ Clean screen — no dark patterns detected!</p>
              </div>
            )}

            {/* OCR text */}
            <details className="bg-gray-900 border border-gray-800 rounded-xl p-4">
              <summary className="text-xs text-gray-500 cursor-pointer">OCR Text Extracted</summary>
              <p className="text-xs text-gray-400 mt-2 font-mono">{result.ocr_text}</p>
            </details>
          </div>
        )}
      </div>
    </div>
  )
}