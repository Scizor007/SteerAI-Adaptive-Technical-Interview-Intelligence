import type { ReactNode } from 'react';
import { Navbar } from './Navbar';

interface AppLayoutProps {
  children: ReactNode;
  fullBleed?: boolean;
  hideNav?: boolean;
}

export function AppLayout({ children, fullBleed = false, hideNav = false }: AppLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col bg-bg-primary">
      {!hideNav && <Navbar fullBleed={fullBleed} />}
      <main className={fullBleed ? 'flex-1' : 'container-steer flex-1 py-8 lg:py-12'}>
        {children}
      </main>
    </div>
  );
}
