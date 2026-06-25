"use client";

import {
  Terminal,
  Cpu,
  GitBranch,
  ArrowRight,
  ShieldCheck,
  Database,
} from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 font-sans selection:bg-indigo-500/30">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/70 backdrop-blur">
        <div className="max-w-6xl mx-auto h-16 px-6 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Cpu className="w-5 h-5 text-indigo-500" />
            <span>RepoMind</span>
          </div>

          <div className="flex gap-6 text-sm text-zinc-400">
            <Link href="#features" className="hover:text-white transition">
              Features
            </Link>

            <Link
              href="/docs/quick-start"
              className="hover:text-white transition"
            >
              Documentation
            </Link>

            <a
              href="https://github.com/Noman-Ahmad25/repomind"
              target="_blank"
              rel="noreferrer"
              className="hover:text-white transition"
            >
              GitHub
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}

      <main className="max-w-6xl mx-auto px-6 py-24 flex flex-col items-center text-center">

        <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-sm text-indigo-400 mb-8">
          🚀 Evidence-first Engineering Intelligence
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-gradient-to-br from-white via-white to-zinc-500 bg-clip-text text-transparent">
          Understand what your
          <br />
          repository needs next.
        </h1>

        <p className="max-w-3xl text-lg md:text-xl text-zinc-400 leading-relaxed mb-10">
          RepoMind combines deterministic static analysis with AI-assisted
          engineering reasoning to identify technical debt, calculate repository
          health, prioritize engineering improvements, and generate actionable
          implementation blueprints.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-20">
          <Link
            href="/docs/installation"
            className="flex items-center gap-2 rounded-md bg-white px-6 py-3 font-semibold text-black hover:bg-zinc-200 transition"
          >
            Get Started
            <ArrowRight className="w-4 h-4" />
          </Link>

          <Link
            href="/docs/quick-start"
            className="flex items-center gap-2 rounded-md border border-zinc-800 bg-zinc-900 px-6 py-3 font-semibold hover:bg-zinc-800 transition"
          >
            <Terminal className="w-4 h-4" />
            Documentation
          </Link>
        </div>

        {/* Terminal */}

        <div className="w-full max-w-4xl overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900 shadow-2xl text-left">

          <div className="flex items-center gap-2 border-b border-zinc-800 bg-zinc-950/50 px-4 py-3">
            <div className="h-3 w-3 rounded-full bg-red-500/40" />
            <div className="h-3 w-3 rounded-full bg-yellow-500/40" />
            <div className="h-3 w-3 rounded-full bg-green-500/40" />

            <span className="ml-2 font-mono text-xs text-zinc-500">
              repomind analyze
            </span>
          </div>

          <div className="space-y-3 p-6 font-mono text-sm">

            <p className="text-zinc-500">
              $ repomind analyze https://github.com/fastapi/fastapi
            </p>

            <p className="text-green-400">
              ✓ Repository cloned successfully
            </p>

            <p className="text-green-400">
              ✓ Parsed 1129 files • 710 classes • 4833 functions
            </p>

            <p className="text-green-400">
              ✓ Reused 11484 cached embeddings
            </p>

            <p className="text-indigo-400">
              Executing deterministic AST audit...
            </p>

            <p className="text-indigo-400">
              Calculating evidence-based health scores...
            </p>

            <div className="space-y-1 text-zinc-300">

              <p>Architecture: 82/100</p>

              <p>Security: 91/100</p>

              <p>Documentation: 85/100</p>

            </div>

            <p className="text-yellow-400 mt-3">
              Top Findings
            </p>

            <p>• GOD_FILE — fastapi/routing.py</p>

            <p>• HIGH_COMPLEXITY — get_request_handler()</p>

            <p>• BROAD_EXCEPTION — get_request_handler()</p>

            <p className="pt-2 text-green-400">
              Generating engineering recommendations...
            </p>

          </div>
        </div>
      </main>

      {/* Features */}

      <section
        id="features"
        className="border-t border-zinc-900 bg-zinc-950/50 py-24"
      >
        <div className="max-w-6xl mx-auto px-6">

          <h2 className="mb-12 text-center text-3xl font-bold">
            Built for Modern Engineering Teams
          </h2>

          <div className="grid gap-6 md:grid-cols-3">

            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">

              <ShieldCheck className="mb-4 h-8 w-8 text-indigo-400" />

              <h3 className="mb-2 text-lg font-semibold">
                Deterministic Analysis
              </h3>

              <p className="text-sm text-zinc-400">
                Python AST powers evidence-based repository analysis, including
                complexity, nesting, security patterns, God File detection, and
                deterministic health scoring.
              </p>

            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">

              <Database className="mb-4 h-8 w-8 text-indigo-400" />

              <h3 className="mb-2 text-lg font-semibold">
                Dockerized Knowledge Base
              </h3>

              <p className="text-sm text-zinc-400">
                PostgreSQL and pgvector store repository metadata, engineering
                findings, and semantic embeddings while automatically reusing
                cached vectors across analyses.
              </p>

            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">

              <GitBranch className="mb-4 h-8 w-8 text-indigo-400" />

              <h3 className="mb-2 text-lg font-semibold">
                AI Engineering Intelligence
              </h3>

              <p className="text-sm text-zinc-400">
                AI transforms verified findings into engineering
                recommendations and implementation blueprints instead of
                performing the static analysis itself.
              </p>

            </div>

          </div>

        </div>
      </section>
    </div>
  );
}

