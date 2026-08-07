import { Link, useLocation } from 'react-router-dom';
import { Layers } from 'lucide-react';
import { BRAND } from '../constants/designTokens';
import { Button } from '../components/ui';

const NAV_LINKS = [
  { to: '/', label: 'Home' },
  { to: '/candidates', label: 'Candidates' },
  { to: '/architecture', label: 'Architecture' },
];

export function Navbar() {
  const { pathname } = useLocation();

  return (
    <header className="sticky top-0 z-50 border-b border-border/80 bg-bg-primary/80 backdrop-blur-xl">
      <div className="container-steer flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent/10 text-accent transition-colors group-hover:bg-accent/20">
            <Layers size={16} strokeWidth={2.25} />
          </div>
          <div className="leading-tight">
            <span className="font-display text-base font-semibold tracking-tight text-text-primary">
              {BRAND.name}
            </span>
            <span className="hidden sm:block text-[11px] text-text-secondary">{BRAND.tagline}</span>
          </div>
        </Link>

        <nav className="hidden items-center gap-1 md:flex" aria-label="Main">
          {NAV_LINKS.map((link) => {
            const active = pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`rounded-lg px-3.5 py-2 text-sm font-medium transition-colors ${
                  active
                    ? 'bg-surface text-text-primary'
                    : 'text-text-secondary hover:text-text-primary hover:bg-surface/50'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <Link to="/candidates">
          <Button variant="primary" size="sm">
            Start Assessment
          </Button>
        </Link>
      </div>
    </header>
  );
}
