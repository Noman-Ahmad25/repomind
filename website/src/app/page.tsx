import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  Brain,
  Code2,
  Cpu,
  Database,
  FileText,
  Gauge,
  GitBranch,
  Layers,
  ShieldCheck,
  Terminal,
} from "lucide-react";

import { CodeBlock, FeatureCard, StatCard } from "@/components/docs";

export const metadata: Metadata = {
  title: "RepoMind - Repository Intelligence",
  description:
    "RepoMind turns deterministic repository analysis into health scores, AI-assisted recommendations, implementation blueprints, and Markdown reports.",
  openGraph: {
    title: "RepoMind - Repository Intelligence",
    description:
      "Deterministic AST analysis, health scoring, AI issue synthesis, blueprints, and Markdown reports for engineering teams.",
    url: "/",
  },
};

const terminalPreview = `$ docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json

RepoMind AI  ·  Static Analysis & Intelligence
══════════════════════════════════════════════════════════
    Target            https://github.com/fastapi/fastapi
    Rules             rules_relaxed.json

Clone
──────────────────────────────────────────────────────────
  →  Fetching latest commits...
  ✔  Cloned to repositories/fastapi_fastapi
    Record ID         42

Scan
──────────────────────────────────────────────────────────
  →  Running single-pass AST scan...
    Project Type      Python Backend/Script
    Languages         Python
    Files Parsed      1129
    Functions Found   4833

Health Scores
──────────────────────────────────────────────────────────
    Architecture     ████████████████░░░░   82/100
    Testing          ███████████████░░░░░   77/100
    Security         ██████████████████░░   91/100
    Documentation    █████████████████░░░   85/100
    Scalability      ███████████████████░   96/100
    Overall          █████████████████░░░   88/100

Recommendations
──────────────────────────────────────────────────────────
  ★  Top Priority
  ID      3f7a51c2
  Title   Refactor high-complexity routing flow
  Next    repomind blueprint 3f7a51c2`;

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 selection:bg-indigo-500/30">
      <nav className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/70 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg">
            <Cpu className="h-5 w-5 text-indigo-500" />
            <span>RepoMind</span>
          </Link>

          <div className="flex gap-6 text-sm text-zinc-400">
            <Link href="#features" className="transition hover:text-white">
              Features
            </Link>
            <Link href="/docs/quick-start" className="transition hover:text-white">
              Documentation
            </Link>
            <a
              href="https://github.com/Noman-Ahmad25/repomind"
              target="_blank"
              rel="noreferrer"
              className="transition hover:text-white"
            >
              GitHub
            </a>
          </div>
        </div>
      </nav>

      <main className="mx-auto flex max-w-6xl flex-col items-center px-6 py-24 text-center">
        <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-sm text-indigo-400">
          <ShieldCheck className="h-4 w-4" />
          Evidence-first engineering intelligence
        </div>

        <h1 className="mb-6 bg-gradient-to-br from-white via-white to-zinc-500 bg-clip-text text-5xl font-extrabold tracking-tight text-transparent md:text-7xl">
          Understand what your
          <br />
          repository needs next.
        </h1>

        <p className="mb-10 max-w-3xl text-lg leading-relaxed text-zinc-400 md:text-xl">
          RepoMind combines deterministic AST analysis with AI-assisted
          engineering reasoning to produce repository health scores, prioritized
          recommendations, implementation blueprints, and Markdown reports.
        </p>

        <div className="mb-20 flex flex-col gap-4 sm:flex-row">
          <Link
            href="/docs/installation"
            className="flex items-center justify-center gap-2 rounded-md bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200"
          >
            Get Started
            <ArrowRight className="h-4 w-4" />
          </Link>

          <Link
            href="/docs/commands"
            className="flex items-center justify-center gap-2 rounded-md border border-zinc-800 bg-zinc-900 px-6 py-3 font-semibold transition hover:bg-zinc-800"
          >
            <Terminal className="h-4 w-4" />
            View Commands
          </Link>
        </div>

        <div className="w-full max-w-5xl text-left">
          <CodeBlock
            title="latest CLI output"
            code={terminalPreview}
            language="text"
          />
        </div>
      </main>

      <section
        id="features"
        className="border-t border-zinc-900 bg-zinc-950/50 py-24"
      >
        <div className="mx-auto max-w-6xl px-6">
          <div className="mx-auto mb-12 max-w-3xl text-center">
            <h2 className="text-3xl font-bold">
              Production repository intelligence
            </h2>
            <p className="mt-3 text-zinc-400">
              RepoMind keeps static analysis deterministic and uses AI only
              after evidence has been collected, scored, and stored.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            <FeatureCard icon={Layers} title="Repository Intelligence">
              Clone a repository, parse structure, identify framework context,
              and persist findings for repeatable engineering review.
            </FeatureCard>
            <FeatureCard icon={ShieldCheck} title="Deterministic Analysis">
              Python AST metrics detect complexity, deep nesting, unsafe
              exception patterns, unused imports, and large files.
            </FeatureCard>
            <FeatureCard icon={Gauge} title="Health Scoring">
              Architecture, testing, security, documentation, scalability, and
              overall scores are calculated from rule-based evidence.
            </FeatureCard>
            <FeatureCard icon={Brain} title="Blueprint Generation">
              AI turns verified findings into implementation plans linked to
              prioritized recommendations.
            </FeatureCard>
            <FeatureCard icon={FileText} title="Markdown Reports">
              Export health scores, issues, recommendations, and blueprint
              instructions into shareable Markdown artifacts.
            </FeatureCard>
            <FeatureCard icon={Database} title="Persistent Repository Intelligence">
              PostgreSQL and pgvector store repository metadata, semantic
              embeddings, health reports, findings, and recommendation history.
            </FeatureCard>
          </div>
        </div>
      </section>

      <section className="border-t border-zinc-900 py-20">
        <div className="mx-auto grid max-w-6xl gap-6 px-6 md:grid-cols-4">
          <StatCard
            value="6"
            label="Health scores"
            description="Architecture, testing, security, documentation, scalability, and overall maturity."
          />
          <StatCard
            value="2"
            label="Rule profiles"
            description="Relaxed for day-to-day analysis and strict for release-readiness review."
          />
          <StatCard
            value="5"
            label="CLI workflows"
            description="Analyze, audit, report, blueprint, and blueprint export."
          />
          <StatCard
            value="1"
            label="Persistent knowledge base"
            description="A Dockerized PostgreSQL and pgvector store for repeatable repository intelligence."
          />
        </div>
      </section>

      <section className="border-t border-zinc-900 bg-zinc-950/50 py-24">
        <div className="mx-auto max-w-6xl px-6">
          <div className="mb-10 flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <h2 className="text-3xl font-bold">Supported Languages</h2>
              <p className="mt-3 max-w-2xl text-zinc-400">
                RepoMind is optimized for Python today and already detects
                broader repository context for mixed stacks.
              </p>
            </div>
            <Link
              href="/docs/roadmap"
              className="inline-flex items-center gap-2 text-sm font-medium text-indigo-400 transition hover:text-indigo-300"
            >
              View roadmap
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
              <Code2 className="mb-4 h-7 w-7 text-indigo-400" />
              <h3 className="font-semibold text-zinc-100">Python</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-400">
                Full deterministic AST analysis for functions, imports,
                complexity, nesting, exception handling, and health scoring.
              </p>
            </div>
            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
              <GitBranch className="mb-4 h-7 w-7 text-indigo-400" />
              <h3 className="font-semibold text-zinc-100">JavaScript / Node</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-400">
                Project signature detection for repository context. Full AST
                analysis is planned as part of multi-language support.
              </p>
            </div>
            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
              <Layers className="mb-4 h-7 w-7 text-indigo-400" />
              <h3 className="font-semibold text-zinc-100">More Languages</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-400">
                The scanner is designed around routed language analyzers, making
                incremental multi-language expansion a core roadmap item.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="border-t border-zinc-900 py-20">
        <div className="mx-auto flex max-w-6xl flex-col items-center px-6 text-center">
          <h2 className="text-3xl font-bold">Start with one repository.</h2>
          <p className="mt-3 max-w-2xl text-zinc-400">
            Run the Docker workflow, analyze a known codebase, and export a
            report your team can discuss immediately.
          </p>
          <div className="mt-8 flex flex-col gap-4 sm:flex-row">
            <Link
              href="/docs/installation"
              className="flex items-center justify-center gap-2 rounded-md bg-white px-6 py-3 font-semibold text-black transition hover:bg-zinc-200"
            >
              Install RepoMind
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/docs/examples"
              className="flex items-center justify-center gap-2 rounded-md border border-zinc-800 bg-zinc-900 px-6 py-3 font-semibold transition hover:bg-zinc-800"
            >
              See Examples
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
