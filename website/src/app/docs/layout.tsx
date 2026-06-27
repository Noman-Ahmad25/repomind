import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { Cpu, GitBranch } from "lucide-react";

import { DocsPager } from "@/components/docs-pager";
import { DocsSidebar } from "@/components/docs-sidebar";

export const metadata: Metadata = {
  title: "Documentation",
  description:
    "RepoMind documentation for installation, CLI commands, rule profiles, configuration, architecture, workflow, health scoring, examples, FAQ, and roadmap.",
  openGraph: {
    title: "RepoMind Documentation",
    description:
      "Production documentation for RepoMind repository intelligence workflows.",
    url: "/docs/quick-start",
  },
};

export default function DocsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50">
      <nav className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/75 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg">
            <Cpu className="h-5 w-5 text-indigo-500" />
            <span>RepoMind</span>
          </Link>

          <div className="flex items-center gap-5 text-sm text-zinc-400">
            <Link href="/docs/quick-start" className="text-white">
              Docs
            </Link>
            <a
              href="https://github.com/Noman-Ahmad25/repomind"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 transition hover:text-white"
            >
              <GitBranch className="h-4 w-4" />
              GitHub
            </a>
          </div>
        </div>
      </nav>

      <div className="mx-auto flex w-full max-w-7xl flex-1 flex-col px-6 md:flex-row">
        <DocsSidebar />

        <main className="w-full max-w-4xl flex-1 py-8 md:pl-12">
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            {children}
            <DocsPager />
          </div>
        </main>
      </div>
    </div>
  );
}
