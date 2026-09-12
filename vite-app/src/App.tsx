const Logo = () => (
  <svg width="18" height="18" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M 160 88 L 194 34 L 216 0 L 256 0 L 256 40 L 221.5 93.5 L 200 128 L 256 128 L 256 256 L 96 256 L 96 168 L 64.246 220 L 40 256 L 0 256 L 0 216 L 34 162 L 56 128 L 0 128 L 0 0 L 160 0 Z" fill="rgb(84, 84, 84)" />
  </svg>
);

export default function App() {
  const navLinks = ['About', 'Demo', 'Technology', 'Contact'];

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

      {/* Overlay for better text readability */}
      <div className="absolute inset-0 bg-black/20"></div>

      {/* Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Navbar */}
        <nav className="flex items-center justify-center pt-4 sm:pt-6 px-4 sm:px-8 gap-2 sm:gap-3">
          {/* Logo Container */}
          <div
            className="flex items-center justify-center rounded-full w-10 h-10 sm:w-11 sm:h-11 shrink-0"
            style={{ backgroundColor: '#EDEDED' }}
          >
            <Logo />
          </div>

          {/* Nav Links Container */}
          <div
            className="flex items-center gap-4 sm:gap-10 rounded-xl px-4 sm:px-8 py-2.5 sm:py-3"
            style={{ backgroundColor: '#EDEDED' }}
          >
            {navLinks.map((link) => (
              <a
                key={link}
                href="#"
                className="text-[12px] sm:text-[14px] font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200"
              >
                {link}
              </a>
            ))}
          </div>
        </nav>

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
              href="#"
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
