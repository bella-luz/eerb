export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-6 sm:px-12 py-20 sm:py-32">
        <h1 className="text-4xl sm:text-5xl font-bold mb-8">About EERB</h1>

        <div className="space-y-8">
          <section>
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">The Problem</h2>
            <p className="text-gray-300 leading-relaxed">
              Renewable energy projects are complex. Solar installations, battery storage systems, and load management require careful coordination. A single miscalculation can lead to undersized systems, wasted investments, or project delays spanning weeks of engineering review.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">Our Solution</h2>
            <p className="text-gray-300 leading-relaxed">
              EERB uses AI-powered engineering analysis to detect technical conflicts in renewable energy designs instantly. Our multi-agent system simulates professional engineering review, catching contradictions between load analysis, solar capacity, and battery specifications before they become costly problems.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">Key Features</h2>
            <ul className="space-y-3">
              {[
                'Multi-agent AI architecture for comprehensive analysis',
                'Deterministic calculations for accurate engineering validation',
                'Conflict detection comparing multiple engineering perspectives',
                'Rapid PDF-based project specification review',
                'Professional engineering-grade reporting'
              ].map((feature, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="text-blue-400 font-bold">✓</span>
                  <span className="text-gray-300">{feature}</span>
                </li>
              ))}
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">Target Users</h2>
            <p className="text-gray-300 leading-relaxed">
              Engineers, project managers, and renewable energy professionals who need rapid preliminary technical validation before formal engineering review.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
