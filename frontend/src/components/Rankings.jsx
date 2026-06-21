import { useState, useEffect } from "react"
import axios from "axios"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts"

export default function Rankings() {
  const [data, setData] = useState(null)

  useEffect(() => {
    axios.get("/api/rankings").then(res => setData(res.data))
  }, [])

  const riskColor = (risk) => {
    if (risk === "High") return "text-red-400 bg-red-950 border-red-900"
    if (risk === "Moderate") return "text-yellow-400 bg-yellow-950 border-yellow-900"
    return "text-green-400 bg-green-950 border-green-900"
  }

  const barColor = (score) => {
    if (score > 35) return "#EF4444"
    if (score > 25) return "#EAB308"
    return "#22C55E"
  }

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2 text-gray-200">App NudgeScore Ranking</h2>
      <p className="text-gray-500 text-sm mb-6">
        Based on analysis of 104 labelled screenshots across 5 Indian investment apps.
      </p>

      {!data && <p className="text-gray-500">Loading...</p>}

      {data && (
        <div className="space-y-6">
          {/* Bar Chart */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h3 className="text-sm font-medium text-gray-300 mb-4">NudgeScore by App (Higher = More Manipulative)</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart
                data={data.apps}
                layout="vertical"
                margin={{ left: 20, right: 40 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" horizontal={false} />
                <XAxis type="number" domain={[0, 50]} stroke="#6B7280" />
                <YAxis type="category" dataKey="name" stroke="#6B7280" width={80} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151' }}
                  formatter={(val) => [`${val}`, 'NudgeScore']}
                />
                <Bar dataKey="score" radius={[0, 4, 4, 0]}>
                  {data.apps.map((entry, i) => (
                    <Cell key={i} fill={barColor(entry.score)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Cards */}
          {data.apps.map((app, i) => (
            <div key={app.name} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-gray-500 text-sm font-mono">#{i+1}</span>
                  <h3 className="font-semibold text-white text-lg">{app.name}</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${riskColor(app.risk)}`}>
                    {app.risk} Risk
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-white">{app.score}</p>
                  <p className="text-xs text-gray-500">NudgeScore</p>
                </div>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2 mb-3">
                <div
                  className="h-2 rounded-full transition-all"
                  style={{ width: `${app.score}%`, backgroundColor: barColor(app.score) }}
                />
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Estimated 10-year investor loss</span>
                <span className="text-red-400 font-semibold">{app.loss}</span>
              </div>
            </div>
          ))}

          {/* Legend */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
            <p className="text-xs text-gray-500 mb-3 font-medium">NUDGESCORE LEGEND</p>
            <div className="flex gap-6 text-sm text-gray-300">
              <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-red-500 inline-block"/> High Risk (&gt;35)</span>
              <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-yellow-500 inline-block"/> Moderate (25-35)</span>
              <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-full bg-green-500 inline-block"/> Low Risk (&lt;25)</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}