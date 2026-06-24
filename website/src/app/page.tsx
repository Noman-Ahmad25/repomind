"use client";

import { Terminal, Cpu, GitBranch, ArrowRight, ShieldCheck, Zap } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 font-sans selection:bg-indigo-500/30">
      {/* Navigation */}
      <nav className="border-b border-zinc-800 bg-zinc-950/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-lg tracking-tight">
            <Cpu className="w-5 h-5 text-indigo-500" />
            <span>RepoMind AI</span>
          </div>
          <div className="flex gap-6 text-sm font-medium text-zinc-400">
            <Link href="#features" className="hover:text-white transition-colors">Features</Link>
            <Link href="/docs/quick-start" className="hover:text-white transition-colors">Documentation</Link>
            <a href="https://github.com/yourusername/repomind" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">GitHub</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-5xl mx-auto px-6 py-24 flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-sm font-medium mb-8 border border-indigo-500/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
          </span>
          v0.1.0 MVP is now live
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-gradient-to-br from-white to-zinc-500 bg-clip-text text-transparent">
          Understand what to <br /> build next.
        </h1>
        
        <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mb-10 leading-relaxed">
          An open-source, local-first repository intelligence tool. Analyze your codebase, detect technical debt, and generate AI-powered engineering blueprints instantly from your terminal.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-20">
          <Link href="/docs/installation" className="flex items-center gap-2 bg-white text-black px-6 py-3 rounded-md font-semibold hover:bg-zinc-200 transition-colors">
            Get Started <ArrowRight className="w-4 h-4" />
          </Link>
          <Link href="/docs/quick-start" className="flex items-center gap-2 bg-zinc-900 border border-zinc-800 text-white px-6 py-3 rounded-md font-semibold hover:bg-zinc-800 transition-colors">
            <Terminal className="w-4 h-4" /> View Documentation
          </Link>
        </div>

        {/* Mock Terminal Output */}
        <div className="w-full max-w-3xl bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden text-left shadow-2xl">
          <div className="flex items-center gap-2 px-4 py-3 border-b border-zinc-800 bg-zinc-950/50">
            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
            <span className="ml-2 text-xs font-mono text-zinc-500">repomind analyze</span>
          </div>
          <div className="p-6 font-mono text-sm md:text-base text-zinc-300 space-y-4">
            <p className="text-zinc-500">$ repomind analyze https://github.com/fastapi/typer</p>
            <p className="text-green-400">✓ Repository cloned successfully!</p>
            <p className="text-indigo-400">Executing AI Stage Detection...</p>
            <div>
              <p className="text-zinc-50">Detected Stage: <span className="font-bold text-white">Growth</span></p>
              <p className="text-zinc-400">Overall Health Score: 74/100</p>
            </div>
            <p className="text-yellow-400">★ RECOMMENDED NEXT ACTION ★</p>
            <p className="text-zinc-50 font-bold">Establish Robust CI/CD Pipelines (Priority: 9.5/10)</p>
          </div>
        </div>
      </main>

      {/* Features Section */}
      <section id="features" className="border-t border-zinc-900 bg-zinc-950/50 py-24">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-3xl font-bold mb-12 text-center">Built for Engineering Rigor</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-zinc-900 border border-zinc-800">
              <ShieldCheck className="w-8 h-8 text-indigo-400 mb-4" />
              <h3 className="font-semibold text-lg mb-2">Local-First Architecture</h3>
              <p className="text-zinc-400 text-sm">Your code never leaves your machine. AST parsing and PostgreSQL vector storage happen entirely locally.</p>
            </div>
            <div className="p-6 rounded-xl bg-zinc-900 border border-zinc-800">
              <Zap className="w-8 h-8 text-indigo-400 mb-4" />
              <h3 className="font-semibold text-lg mb-2">Technical Debt Detection</h3>
              <p className="text-zinc-400 text-sm">Go beyond basic linting. Identify architectural bottlenecks and missing testing coverage automatically.</p>
            </div>
            <div className="p-6 rounded-xl bg-zinc-900 border border-zinc-800">
              <GitBranch className="w-8 h-8 text-indigo-400 mb-4" />
              <h3 className="font-semibold text-lg mb-2">Actionable Blueprints</h3>
              <p className="text-zinc-400 text-sm">Don't just find problems. Generate step-by-step implementation plans for the highest priority fixes.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}