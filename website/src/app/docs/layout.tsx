import Link from "next/link";
import { Download, Rocket, GitBranch } from "lucide-react";

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 flex flex-col pt-16">
      <div className="max-w-7xl mx-auto w-full px-6 flex-1 flex flex-col md:flex-row">
        
        {/* Sidebar Navigation */}
        <aside className="w-full md:w-64 py-8 md:pr-8 border-b md:border-b-0 md:border-r border-zinc-800">
          <nav className="space-y-6 sticky top-24">
            <div>
              <h4 className="font-semibold text-zinc-100 mb-3 px-2">Getting Started</h4>
              <ul className="space-y-1 text-sm text-zinc-400">
                <li>
                  <Link href="/docs/installation" className="flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-zinc-900 hover:text-white transition-colors">
                    <Download className="w-4 h-4" /> Installation
                  </Link>
                </li>
                <li>
                  <Link href="/docs/quick-start" className="flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-zinc-900 hover:text-white transition-colors">
                    <Rocket className="w-4 h-4" /> Quick Start
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-zinc-100 mb-3 px-2">Core Concepts</h4>
              <ul className="space-y-1 text-sm text-zinc-400">
                <li>
                  <Link href="/docs/architecture" className="flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-zinc-900 hover:text-white transition-colors">
                    <GitBranch className="w-4 h-4" /> Architecture
                  </Link>
                </li>
              </ul>
            </div>
          </nav>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 py-8 md:pl-12 max-w-3xl">
          {children}
        </main>
        
      </div>
    </div>
  );
}