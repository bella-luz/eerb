export default function DemoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-6 sm:px-12 py-20 sm:py-32">
        <h1 className="text-4xl sm:text-5xl font-bold mb-8">Interactive Demo</h1>

        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">Try EERB Live</h2>
            <p className="text-gray-300 leading-relaxed mb-6">
              Experience the power of AI-driven engineering review. Our demo includes:
            </p>

            <div className="grid md:grid-cols-2 gap-4 mb-8">
              {[
                { title: 'Pre-loaded Project', desc: 'Commercial building with solar and battery' },
                { title: 'Real-time Analysis', desc: 'Multi-agent AI analysis in seconds' },
                { title: 'Conflict Detection', desc: 'Identifies technical inconsistencies' },
                { title: 'Export Reports', desc: 'Professional engineering findings' }
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 border border-blue-400/30 rounded-lg p-4">
                  <h3 className="text-blue-300 font-semibold mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-400">{item.desc}</p>
                </div>
              ))}
            </div>

            <a
              href="https://6wkzs3zlyitwuzhdq2vtzc.streamlit.app"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-base font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-full px-8 py-3 transition-all duration-200"
            >
              Open Live Demo
              <span>→</span>
            </a>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">How It Works</h2>
            <div className="space-y-4">
              {[
                { num: '1', title: 'Upload Project', desc: 'Provide project specifications (PDF or CSV)' },
                { num: '2', title: 'AI Analysis', desc: '6 specialized agents review the design' },
                { num: '3', title: 'Conflict Check', desc: 'Independent critic verifies findings' },
                { num: '4', title: 'Get Report', desc: 'Download professional engineering report' }
              ].map((step, i) => (
                <div key={i} className="flex gap-4">
                  <div className="flex-shrink-0">
                    <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-600">
                      {step.num}
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-blue-300">{step.title}</h3>
                    <p className="text-sm text-gray-400">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
