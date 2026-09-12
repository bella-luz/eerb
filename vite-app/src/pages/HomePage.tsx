export default function HomePage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#f0f0ee]">
      {/* Background Video */}
      <video
        autoPlay
        muted
        loop
        playsInline
        className="absolute inset-0 w-full h-full object-cover"
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}
      >
        <source
          src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_215831_c6a8989c-d716-4d8d-8745-e972a2eec711.mp4"
          type="video/mp4"
        />
      </video>

      {/* Overlay */}
      <div className="absolute inset-0 bg-black/20"></div>

      {/* Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Hero Content */}
        <div className="flex-1 flex items-end pb-10 sm:pb-16 lg:pb-20 px-6 sm:px-12 md:px-20 lg:px-28">
          <div className="max-w-xs">
            {/* Badge */}
            <a
              href="#"
              className="inline-flex items-center gap-1.5 text-[11.5px] font-medium text-blue-300 hover:text-blue-200 transition-colors mb-3 group"
            >
              AI-Powered Engineering Review
              <span className="inline-block transition-transform duration-200 group-hover:translate-x-0.5">
                →
              </span>
            </a>

            {/* Headline */}
            <h1 className="text-[1.5rem] sm:text-[1.75rem] leading-[1.15] font-medium text-white tracking-tight mb-3">
              AI Engineering Review Before You Build
            </h1>

            {/* Subtext */}
            <p className="text-[13px] text-gray-200 font-normal mb-3">
              Identify technical conflicts in seconds, not weeks.
            </p>

            {/* CTA Button */}
            <a
              href="https://6wkzs3zlyitwuzhdq2vtzc.streamlit.app"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-[13px] font-medium text-white border border-white rounded-full px-5 py-2.5 hover:bg-white hover:text-blue-600 hover:border-white transition-all duration-200 group"
            >
              Start Free Review
              <span className="inline-block transition-transform duration-200 group-hover:translate-x-0.5">
                →
              </span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
