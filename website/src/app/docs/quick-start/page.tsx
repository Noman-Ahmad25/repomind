import type { Metadata } from "next";

import { Callout, CodeBlock, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Quick Start",
  description:
    "Run RepoMind's analyze, audit, report, blueprint, and blueprint export workflow.",
};

const repoUrl = "https://github.com/fastapi/fastapi";

const analyze = `docker compose exec app repomind analyze ${repoUrl} --rules rules_relaxed.json`;

const analyzeOutput = `RepoMind AI  ·  Static Analysis & Intelligence
══════════════════════════════════════════════════════════
    Target            https://github.com/fastapi/fastapi
    Rules             rules_relaxed.json

Clone
──────────────────────────────────────────────────────────
  →  Fetching latest commits...
  ✔  Cloned to repositories/fastapi_fastapi

Scan
──────────────────────────────────────────────────────────
  →  Running single-pass AST scan...
    Project Type      Python Backend/Script
    Languages         Python
    Files Parsed      1129
    Functions Found   4833

Health Scores
──────────────────────────────────────────────────────────
    Architecture      82/100
    Testing           77/100
    Security          91/100
    Documentation     85/100
    Scalability       96/100
    Overall           88/100`;

const audit = `docker compose exec app repomind audit ${repoUrl} --rules rules_relaxed.json`;

const auditOutput = `RepoMind AI  ·  AST Audit
══════════════════════════════════════════════════════════
    Path              repositories/fastapi_fastapi
    Rules             rules_relaxed.json

AST Scan
──────────────────────────────────────────────────────────
  →  Parsing source files and evaluating rule violations...
  12 violation(s)  ·  2.41s
  Ranked by cyclomatic complexity — top 10`;

const report = `docker compose exec app repomind report ${repoUrl}`;

const reportOutput = `RepoMind AI  ·  Report Export
══════════════════════════════════════════════════════════
    Target            https://github.com/fastapi/fastapi

Compile
──────────────────────────────────────────────────────────
  →  Loading health scores, findings, and recommendations...
  →  Rendering Markdown report...
  ✔  Report saved to reports/fastapi_fastapi/analysis_fastapi_fastapi.md`;

const blueprint = `docker compose exec app repomind blueprint <recommendation-id>`;

const blueprintExport = `docker compose exec app repomind blueprint <recommendation-id> --export`;

const reportLocations = `reports/
└── fastapi_fastapi/
    ├── analysis_fastapi_fastapi.md
    ├── blueprint_3f7a51c2.md
    └── ...`;

export default function QuickStartPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Getting Started"
        title="Quick Start"
        description={
          <>
            This workflow runs RepoMind against a repository, reviews
            deterministic findings, exports a Markdown report, and generates an
            implementation blueprint from a recommendation.
          </>
        }
      />

      <Callout title="Use the relaxed rule profile first" variant="tip">
        <code className="text-zinc-100">rules_relaxed.json</code> is the
        recommended starting profile for general repository analysis. Switch to
        the strict profile when you want a more aggressive release-readiness
        review.
      </Callout>

      <Section
        title="1. Analyze"
        description="Run the complete pipeline: clone, AST scan, rule evaluation, health scoring, AI issue synthesis, and recommendation generation."
      >
        <CodeBlock title="analyze" code={analyze} />
        <CodeBlock title="expected output" code={analyzeOutput} language="text" />
      </Section>

      <Section
        title="2. Audit"
        description="Review deterministic AST findings without generating AI recommendations."
      >
        <CodeBlock title="audit" code={audit} />
        <CodeBlock title="expected output" code={auditOutput} language="text" />
      </Section>

      <Section
        title="3. Report"
        description="Export health scores, findings, and prioritized recommendations to Markdown."
      >
        <CodeBlock title="report" code={report} />
        <CodeBlock title="expected output" code={reportOutput} language="text" />
      </Section>

      <Section
        title="4. Blueprint"
        description="Use a recommendation ID from the analyze output to generate a concrete implementation plan."
      >
        <CodeBlock title="blueprint" code={blueprint} />
        <Callout title="Where recommendation IDs come from">
          The <code className="text-zinc-100">analyze</code> command prints
          saved recommendation IDs. Each ID can be passed to{" "}
          <code className="text-zinc-100">repomind blueprint</code>.
        </Callout>
      </Section>

      <Section
        title="5. Blueprint Export"
        description="Add --export to save the generated blueprint as Markdown."
      >
        <CodeBlock title="blueprint export" code={blueprintExport} />
      </Section>

      <Section
        title="Generated Locations"
        description="Reports and exported blueprints are written under a repository-specific folder."
      >
        <CodeBlock title="reports directory" code={reportLocations} language="text" />
      </Section>
    </div>
  );
}
