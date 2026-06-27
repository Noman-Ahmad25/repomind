import type { Metadata } from "next";

import { Callout, CodeBlock, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Examples",
  description:
    "Complete RepoMind example workflows with commands, expected outputs, generated reports, and blueprints.",
};

const commands = `docker compose up -d app
docker compose exec app alembic upgrade head
docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json
docker compose exec app repomind audit https://github.com/fastapi/fastapi --rules rules_relaxed.json
docker compose exec app repomind report https://github.com/fastapi/fastapi
docker compose exec app repomind blueprint 3f7a51c2 --export`;

const analyzeOutput = `Health Scores
──────────────────────────────────────────────────────────
    Architecture      82/100
    Testing           77/100
    Security          91/100
    Documentation     85/100
    Scalability       96/100
    Overall           88/100

Recommendations
──────────────────────────────────────────────────────────
  ★  Top Priority
  ID      3f7a51c2
  Title   Refactor high-complexity routing flow
  Score   Priority 9.2/10  ·  Impact 8.8  ·  Effort 6.0`;

const report = `# Repository Intelligence Report: fastapi/fastapi

**Repository:** https://github.com/fastapi/fastapi

## Health Analysis

- **Overall Maturity:** 88/100
- **Architecture:** 82/100
- **Testing:** 77/100
- **Security:** 91/100
- **Documentation:** 85/100
- **Scalability:** 96/100

## Prioritized Recommendations

### ★ RECOMMENDED NEXT ACTION: Refactor high-complexity routing flow

**Priority:** 9.2/10 (Impact: 8.8 | Effort: 6.0)

To generate a blueprint for this recommendation, run:
\`repomind blueprint 3f7a51c2\``;

const blueprint = `# Implementation Blueprint: Refactor high-complexity routing flow

**Goal:** Reduce request routing complexity while preserving public behavior.

## Files to Create

- \`tests/test_routing_refactor.py\`

## Files to Modify

- \`fastapi/routing.py\`

## Implementation Steps

1. Extract request validation into a focused helper.
2. Add regression tests around existing routing behavior.
3. Replace nested conditionals with named decision functions.

**Estimated Effort:** Medium`;

const locations = `reports/
└── fastapi_fastapi/
    ├── analysis_fastapi_fastapi.md
    └── blueprint_3f7a51c2.md`;

export default function ExamplesPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Reference"
        title="Examples"
        description={
          <>
            This example uses FastAPI to show a complete Docker workflow from
            analysis to report and blueprint export.
          </>
        }
      />

      <Callout title="Example IDs vary">
        Recommendation IDs, scores, and finding counts depend on the repository
        version and rule profile. Treat the snippets as representative output.
      </Callout>

      <Section title="FastAPI Workflow" description="Commands executed in order.">
        <CodeBlock title="commands" code={commands} />
      </Section>

      <Section title="Expected Analysis Output">
        <CodeBlock title="analyze output" code={analyzeOutput} language="text" />
      </Section>

      <Section title="Generated Report">
        <p className="mb-3 leading-7 text-zinc-400">
          The report command writes a Markdown file that summarizes health,
          findings, and recommendations.
        </p>
        <CodeBlock title="analysis_fastapi_fastapi.md" code={report} language="markdown" />
      </Section>

      <Section title="Blueprint Export">
        <p className="mb-3 leading-7 text-zinc-400">
          The blueprint export turns a recommendation into an implementation
          plan that can be reviewed or handed to an engineer.
        </p>
        <CodeBlock title="blueprint_3f7a51c2.md" code={blueprint} language="markdown" />
      </Section>

      <Section title="Generated Files">
        <CodeBlock title="reports" code={locations} language="text" />
      </Section>
    </div>
  );
}
