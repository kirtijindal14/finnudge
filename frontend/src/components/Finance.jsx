import { useState, useEffect } from "react"
import axios from "axios"
import API from '../api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from "recharts"

export default function Finance() {
  const [monthly, setMonthly] = useState(5000)
  const [years, setYears] = useState(10)
  const [app, setApp] = useState("Groww")
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchData = async () => {
    setLoading(true)
    try {
      const res = await axios.get(`${API}/api/finance?monthly=${monthly}&years=${years}&app=${app}`)
      setData(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  useEffect(() => { fetchData() }, [])

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2 text-gray-200">Calculate Your Dark Pattern Cost</h2>
      <p className="text-gray-500 text-sm mb-6">See how much dark patterns could cost you over time.</p>

      {/* Controls */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <label className="text-xs text-gray-500 block mb-2">Monthly SIP (₹)</label>
          <input
            type="range" min={1000} max={20000} step={500}
            value={monthly} onChange={e => setMonthly(Number(e.target.value))}
            className="w-full accent-blue-500"
          />
          <p className="text-white font-bold mt-1">₹{monthly.toLocaleString()}</p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <label className="text-xs text-gray-500 block mb-2">Investment Horizon</label>
          <input
            type="range" min={1} max={20} step={1}
            value={years} onChange={e => setYears(Number(e.target.value))}
            className="w-full accent-blue-500"
          />
          <p className="text-white font-bold mt-1">{years} years</p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
          <label className="text-xs text-gray-500 block mb-2">App You Use</label>
          <select
            value={app} onChange={e => setApp(e.target.value)}
            className="w-full bg-gray-800 text-white rounded-lg px-3 py-2 border border-gray-700 mt-1"
          >
            {["Groww","AngelOne","INDmoney","Upstox","Zerodha"].map(a => (
              <option key={a}>{a}</option>
            ))}
          </select>
        </div>
      </div>

      <button
        onClick={fetchData}
        className="mb-6 bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg transition-colors"
      >
        Calculate
      </button>

      {loading && <p className="text-gray-500">Calculating...</p>}

      {data && !loading && (
        <div className="space-y-6">
          {/* Metrics */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
              <p className="text-xs text-gray-500 mb-1">Without Dark Patterns</p>
              <p className="text-xl font-bold text-green-400">₹{data.clean.toLocaleString()}</p>
            </div>
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
              <p className="text-xs text-gray-500 mb-1">With Dark Patterns</p>
              <p className="text-xl font-bold text-red-400">₹{data.nudged.toLocaleString()}</p>
            </div>
            <div className="bg-red-950 border border-red-900 rounded-xl p-4 text-center">
              <p className="text-xs text-red-400 mb-1">Hidden Cost</p>
              <p className="text-xl font-bold text-red-300">₹{data.loss.toLocaleString()}</p>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h3 className="text-sm font-medium text-gray-300 mb-4">
              Wealth Gap — {app} vs Rational Investor
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.chart_data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="year" stroke="#6B7280" label={{ value: 'Years', position: 'insideBottom', offset: -2, fill: '#6B7280' }} />
                <YAxis stroke="#6B7280" label={{ value: '₹ Lakhs', angle: -90, position: 'insideLeft', fill: '#6B7280' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151' }}
                  formatter={(val) => [`₹${val}L`, '']}
                />
                <Legend />
                <Line type="monotone" dataKey="clean" stroke="#10B981" strokeWidth={2} name="Rational Investor" dot={false} />
                <Line type="monotone" dataKey="nudged" stroke="#EF4444" strokeWidth={2} name={`${app} User`} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}