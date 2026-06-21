import { useState } from "react"
import Analyser from "./components/Analyser"
import Rankings from "./components/Rankings"
import Finance from "./components/Finance"

export default function App() {
  const [activeTab, setActiveTab] = useState("analyse")

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">🔍 FinNudge</h1>
            <p className="text-gray-400 text-sm">Behavioural Finance Audit of Indian Investment Apps</p>
          </div>
          <span className="text-xs text-gray-500">Built by Kirti Jindal | NSUT Delhi</span>
        </div>
      </div>

      <div className="bg-gray-900 border-b border-gray-800 px-6">
        <div className="max-w-6xl mx-auto flex gap-1">
          {[
            { id: "analyse", label: "🔍 Analyse Screenshot" },
            { id: "rankings", label: "📊 App Rankings" },
            { id: "finance", label: "💰 Finance Impact" },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab.id
                  ? "border-blue-500 text-blue-400"
                  : "border-transparent text-gray-400 hover:text-gray-200"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {activeTab === "analyse" && <Analyser />}
        {activeTab === "rankings" && <Rankings />}
        {activeTab === "finance" && <Finance />}
      </div>
    </div>
  )
}