import { Link } from 'react-router-dom';

const Logo = () => (
  <svg width="18" height="18" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M 160 88 L 194 34 L 216 0 L 256 0 L 256 40 L 221.5 93.5 L 200 128 L 256 128 L 256 256 L 96 256 L 96 168 L 64.246 220 L 40 256 L 0 256 L 0 216 L 34 162 L 56 128 L 0 128 L 0 0 L 160 0 Z" fill="rgb(84, 84, 84)" />
  </svg>
);

export default function Navigation() {
  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'About', path: '/about' },
    { name: 'Demo', path: '/demo' },
    { name: 'Technology', path: '/technology' },
    { name: 'Contact', path: '/contact' }
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-center pt-4 sm:pt-6 px-4 sm:px-8 gap-2 sm:gap-3 bg-white/5 backdrop-blur-sm">
      {/* Logo Container */}
      <Link
        to="/"
        className="flex items-center justify-center rounded-full w-10 h-10 sm:w-11 sm:h-11 shrink-0 bg-white hover:bg-gray-100 transition-colors duration-200"
      >
        <Logo />
      </Link>

      {/* Nav Links Container */}
      <div className="flex items-center gap-4 sm:gap-6 rounded-xl px-4 sm:px-8 py-2.5 sm:py-3 bg-white/90 backdrop-blur-sm">
        {navLinks.map((link) => (
          <Link
            key={link.name}
            to={link.path}
            className="text-[12px] sm:text-[14px] font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200"
          >
            {link.name}
          </Link>
        ))}
      </div>
    </nav>
  );
}
