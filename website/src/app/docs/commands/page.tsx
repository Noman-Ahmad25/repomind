import type { Metadata } from "next";

import { Callout, CodeBlock, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Commands",
  description:
    "Complete RepoMind CLI command reference for analyze, audit, report, blueprint, and blueprint export.",
};

type CommandDoc = {
  name: string;
  purpose: string;
  syntax: string;
  arguments: { name: string; description: string }[];
  example: string;
  output: string;
  notes: string[];
};

const commands: CommandDoc[] = [
  {
    name: "analyze",
    purpose:
      "Run the full repository intelligence pipeline: clone or update the repository, scan source code, evaluate deterministic rules, calculate health scores, synthesize AI issues, and save prioritized recommendations.",
    syntax:
      "repomind analyze <repository_url> --rules rules_relaxed.json",
    arguments: [
      {
        name: "repository_url",
        description:
          "Required GitHub repository URL in the form https://github.com/<owner>/<repo>.",
      },
      {
        name: "--rules, -r",
        description:
          "Path to a rule profile JSON file. Use rules_relaxed.json for normal analysis or rules_strict.json for stricter thresholds.",
      },
    ],
    example:
      "docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json",
    output: `RepoMind AI  ·  Static Analysis & Intelligence
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
    Overall           88/100

Recommendations
──────────────────────────────────────────────────────────
  ID      3f7a51c2
  Next    repomind blueprint 3f7a51c2`,
    notes: [
      "Requires GEMINI_API_KEY because issue synthesis and recommendations use the AI layer.",
      "Persists repository metadata, health scores, findings, and recommendations to PostgreSQL.",
      "Use this command before report or blueprint so the database has saved analysis state.",
    ],
  },
  {
    name: "audit",
    purpose:
      "Run a fast deterministic AST audit without AI issue synthesis or recommendation generation.",
    syntax: "repomind audit <repository_url> --rules rules_relaxed.json",
    arguments: [
      {
        name: "repository_url",
        description:
          "Required GitHub repository URL. RepoMind reuses the local cached clone when available.",
      },
      {
        name: "--rules, -r",
        description:
          "Path to the rule profile used for threshold evaluation.",
      },
    ],
    example:
      "docker compose exec app repomind audit https://github.com/fastapi/fastapi --rules rules_relaxed.json",
    output: `RepoMind AI  ·  AST Audit
══════════════════════════════════════════════════════════
    Path              repositories/fastapi_fastapi
    Rules             rules_relaxed.json

AST Scan
──────────────────────────────────────────────────────────
  →  Parsing source files and evaluating rule violations...

  12 violation(s)  ·  2.41s
  Ranked by cyclomatic complexity — top 10

  [ 1] get_request_handler
       File        fastapi/routing.py
       Complexity  31
       Nesting     6
       Violations  HIGH_COMPLEXITY, DEEP_NESTING`,
    notes: [
      "Does not call Gemini and is useful for quick local validation.",
      "Prints the top deterministic findings ranked by complexity.",
      "Run analyze when you want the same evidence synthesized into recommendations.",
    ],
  },
  {
    name: "report",
    purpose:
      "Generate a Markdown repository intelligence report from a previously analyzed repository.",
    syntax: "repomind report <repository_url>",
    arguments: [
      {
        name: "repository_url",
        description:
          "Required GitHub repository URL. It must match a repository already analyzed and saved in PostgreSQL.",
      },
    ],
    example:
      "docker compose exec app repomind report https://github.com/fastapi/fastapi",
    output: `RepoMind AI  ·  Report Export
══════════════════════════════════════════════════════════
    Target            https://github.com/fastapi/fastapi

Compile
──────────────────────────────────────────────────────────
  →  Loading health scores, findings, and recommendations...
  →  Rendering Markdown report...

  ✔  Report saved to reports/fastapi_fastapi/analysis_fastapi_fastapi.md`,
    notes: [
      "Run analyze first so health scores, findings, and recommendations exist.",
      "Reports are saved under reports/<owner>_<repository>/.",
      "The report includes health analysis, discovered issues, and prioritized recommendations.",
    ],
  },
  {
    name: "blueprint",
    purpose:
      "Generate an implementation plan for a saved recommendation ID.",
    syntax: "repomind blueprint <recommendation_id>",
    arguments: [
      {
        name: "recommendation_id",
        description:
          "Required recommendation ID printed by analyze and stored in PostgreSQL.",
      },
    ],
    example:
      "docker compose exec app repomind blueprint 3f7a51c2",
    output: `RepoMind AI  ·  Implementation Blueprint
══════════════════════════════════════════════════════════
    Recommendation    Refactor high-complexity routing flow
    ID                3f7a51c2

Generate
──────────────────────────────────────────────────────────
  →  Synthesizing implementation plan from linked findings...

Blueprint
──────────────────────────────────────────────────────────
  Goal
    Reduce request routing complexity while preserving public behavior.

  Files to Create
    +  tests/test_routing_refactor.py

  Implementation Steps
     1.  Extract request validation into a focused helper.
     2.  Add regression tests around existing routing behavior.
     3.  Replace nested conditionals with named decision functions.

  Estimated Effort  Medium`,
    notes: [
      "Requires a recommendation generated by analyze.",
      "Persists the blueprint JSON in the blueprints table.",
      "Use --export when you want a Markdown artifact on disk.",
    ],
  },
  {
    name: "blueprint --export",
    purpose:
      "Generate a blueprint and save it as Markdown under the repository report folder.",
    syntax: "repomind blueprint <recommendation_id> --export",
    arguments: [
      {
        name: "recommendation_id",
        description: "Required saved recommendation ID.",
      },
      {
        name: "--export, -e",
        description:
          "Writes the generated blueprint to reports/<owner>_<repository>/blueprint_<id>.md.",
      },
    ],
    example:
      "docker compose exec app repomind blueprint 3f7a51c2 --export",
    output: `Export
──────────────────────────────────────────────────────────
  →  Rendering blueprint to Markdown...
  ✔  Blueprint saved to reports/fastapi_fastapi/blueprint_3f7a51c2.md`,
    notes: [
      "The exported file contains the goal, files to create, files to modify, implementation steps, and estimated effort.",
      "Generated filenames use the first eight characters of the recommendation ID.",
      "Blueprint exports are useful for implementation planning, review, or handoff.",
    ],
  },
];

function CommandSection({ command }: { command: CommandDoc }) {
  return (
    <Section title={command.name} description={command.purpose}>
      <div className="space-y-5">
        <div>
          <h3 className="mb-3 font-semibold text-zinc-100">Syntax</h3>
          <CodeBlock title="syntax" code={command.syntax} />
        </div>

        <div>
          <h3 className="mb-3 font-semibold text-zinc-100">Arguments</h3>
          <div className="overflow-hidden rounded-lg border border-zinc-800">
            <div className="divide-y divide-zinc-800">
              {command.arguments.map((argument) => (
                <div
                  key={argument.name}
                  className="grid gap-2 bg-zinc-900 p-4 sm:grid-cols-[180px_1fr]"
                >
                  <code className="font-mono text-sm text-indigo-300">
                    {argument.name}
                  </code>
                  <p className="text-sm leading-6 text-zinc-400">
                    {argument.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div>
          <h3 className="mb-3 font-semibold text-zinc-100">Example</h3>
          <CodeBlock title="command" code={command.example} />
        </div>

        <div>
          <h3 className="mb-3 font-semibold text-zinc-100">Output</h3>
          <CodeBlock title="output" code={command.output} language="text" />
        </div>

        <div>
          <h3 className="mb-3 font-semibold text-zinc-100">Notes</h3>
          <ul className="space-y-2 text-sm leading-6 text-zinc-400">
            {command.notes.map((note) => (
              <li key={note} className="rounded-lg border border-zinc-800 bg-zinc-900/60 p-3">
                {note}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Section>
  );
}

export default function CommandsPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Guides"
        title="Commands"
        description={
          <>
            RepoMind is a Typer-based CLI with commands for full analysis,
            deterministic audit, Markdown reporting, and implementation
            blueprint generation.
          </>
        }
      />

      <Callout title="Docker examples">
        Examples use <code className="text-zinc-100">docker compose exec app</code>
        because Docker is the recommended installation path. In a manual setup,
        run the same commands with <code className="text-zinc-100">uv run</code>
        or the installed <code className="text-zinc-100">repomind</code> entry
        point.
      </Callout>

      {commands.map((command) => (
        <CommandSection key={command.name} command={command} />
      ))}
    </div>
  );
}
