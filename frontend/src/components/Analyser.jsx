export default function Analyser() {
  return (
    <div className="text-center py-20">
      <p className="text-6xl mb-6">🔍</p>
      <h2 className="text-2xl font-bold text-white mb-3">Screenshot Analyser</h2>
      <p className="text-gray-400 mb-2 max-w-lg mx-auto">
        Upload any Indian investment app screenshot to detect dark patterns and calculate their financial impact.
      </p>
      <p className="text-gray-600 text-sm mb-8 max-w-lg mx-auto">
        Powered by CLIP vision embeddings + OCR text analysis
      </p>
      
        href="https://finnudge.streamlit.app"
        target="_blank"
        rel="noopener noreferrer"
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-10 py-4 rounded-xl transition-colors inline-block text-lg"
      >
        Launch Analyser →
      </a>
      <p className="text-gray-600 text-xs mt-4">Opens in a new tab</p>
    </div>
  )
}
