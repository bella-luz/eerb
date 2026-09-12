export default function ContactPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-6 sm:px-12 py-20 sm:py-32">
        <h1 className="text-4xl sm:text-5xl font-bold mb-8">Get in Touch</h1>

        <div className="grid md:grid-cols-2 gap-12 mb-12">
          <div>
            <h2 className="text-2xl font-semibold mb-6 text-blue-400">Contact Information</h2>
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-blue-300 mb-2">Project Repository</h3>
                <a
                  href="https://github.com/bella-luz/eerb"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-blue-400 transition-colors"
                >
                  github.com/bella-luz/eerb
                </a>
              </div>
              <div>
                <h3 className="font-semibold text-blue-300 mb-2">Live Application</h3>
                <a
                  href="https://6wkzs3zlyitwuzhdq2vtzc.streamlit.app"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-blue-400 transition-colors"
                >
                  EERB Demo on Streamlit Cloud
                </a>
              </div>
              <div>
                <h3 className="font-semibold text-blue-300 mb-2">Technology Stack</h3>
                <p className="text-gray-300">
                  Python • Streamlit • React • TypeScript • OpenAI API • Vercel
                </p>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-6 text-blue-400">About This Project</h2>
            <div className="space-y-4 text-gray-300">
              <p>
                EERB was built as a hackathon project to demonstrate AI-powered engineering review for renewable energy systems.
              </p>
              <p>
                Our mission is to make professional-grade engineering validation accessible and fast, helping accelerate renewable energy deployment worldwide.
              </p>
              <p className="text-sm text-gray-400 mt-6 italic">
                Note: EERB is a preliminary engineering review tool and should not replace professional engineering consultation.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-blue-900/20 border border-blue-400/30 rounded-lg p-8">
          <h2 className="text-2xl font-semibold mb-6 text-blue-400">Ready to Try EERB?</h2>
          <p className="text-gray-300 mb-6">
            Upload your renewable energy project specifications and get AI-powered engineering analysis in seconds.
          </p>
          <a
            href="https://6wkzs3zlyitwuzhdq2vtzc.streamlit.app"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-base font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-full px-8 py-3 transition-all duration-200"
          >
            Open EERB App
            <span>→</span>
          </a>
        </div>
      </div>
    </div>
  );
}
