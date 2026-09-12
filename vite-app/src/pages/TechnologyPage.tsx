export default function TechnologyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-6 sm:px-12 py-20 sm:py-32">
        <h1 className="text-4xl sm:text-5xl font-bold mb-8">Technology</h1>

        <div className="space-y-12">
          <section>
            <h2 className="text-2xl font-semibold mb-6 text-blue-400">Architecture</h2>
            <div className="space-y-4">
              {[
                { layer: 'Frontend', tech: 'React + TypeScript + Tailwind CSS', desc: 'Modern, responsive user interface' },
                { layer: 'Backend', tech: 'Streamlit + Python', desc: 'Rapid deployment and data visualization' },
                { layer: 'AI Engine', tech: 'OpenAI GPT + Multi-Agent System', desc: '6 specialized engineering agents' },
                { layer: 'Calculations', tech: 'Pure Python Math', desc: 'Deterministic engineering analysis' },
                { layer: 'Data', tech: 'CSV + PDF + JSON', desc: 'Flexible project specification formats' }
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 border border-blue-400/30 rounded-lg p-4">
                  <h3 className="text-blue-300 font-semibold">{item.layer}</h3>
                  <p className="text-sm text-gray-400">{item.tech}</p>
                  <p className="text-xs text-gray-500 mt-1">{item.desc}</p>
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-6 text-blue-400">Multi-Agent System</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {[
                { agent: 'Load Analyst', role: 'Analyzes building/facility power demand profiles' },
                { agent: 'PV Engineer', role: 'Evaluates solar generation capacity and sizing' },
                { agent: 'BESS Engineer', role: 'Designs battery storage systems and discharge duration' },
                { agent: 'Specification Engineer', role: 'Extracts requirements from project documents' },
                { agent: 'Independent Critic', role: 'Challenges findings and identifies conflicts' },
                { agent: 'Lead Engineer', role: 'Synthesizes analysis into final report' }
              ].map((item, i) => (
                <div key={i} className="bg-blue-900/30 border border-blue-400/50 rounded-lg p-4">
                  <h3 className="text-blue-300 font-semibold mb-2">{item.agent}</h3>
                  <p className="text-sm text-gray-300">{item.role}</p>
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-6 text-blue-400">Key Technologies</h2>
            <div className="grid sm:grid-cols-2 gap-4">
              {[
                'React 18 for interactive UI',
                'Streamlit for rapid deployment',
                'OpenAI GPT-3.5 for AI reasoning',
                'Python for deterministic calculations',
                'PDF text extraction with keyword RAG',
                'Vercel for frontend hosting',
                'Streamlit Cloud for backend'
              ].map((tech, i) => (
                <div key={i} className="flex items-start gap-3">
                  <span className="text-blue-400 font-bold flex-shrink-0">◆</span>
                  <span className="text-gray-300">{tech}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="bg-blue-900/20 border border-blue-400/30 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 text-blue-400">Why This Architecture?</h2>
            <ul className="space-y-2 text-gray-300">
              <li>• <strong>Distributed AI:</strong> Multiple agents provide diverse perspectives on technical issues</li>
              <li>• <strong>Conflict Detection:</strong> Independent critic compares agent outputs to find contradictions</li>
              <li>• <strong>Deterministic Validation:</strong> Pure math ensures reproducible engineering calculations</li>
              <li>• <strong>Rapid Deployment:</strong> Streamlit + Vercel enable quick iteration and updates</li>
              <li>• <strong>User-Friendly:</strong> Intuitive interface for non-technical stakeholders</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}
