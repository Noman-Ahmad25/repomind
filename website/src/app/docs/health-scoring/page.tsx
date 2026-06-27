import type { Metadata } from "next";

import { Callout, PageHeader, ScoreBar, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Health Scoring",
  description:
    "Understand RepoMind's architecture, testing, security, documentation, scalability, and overall health scores.",
};

const scoreRows = [
  {
    score: "Architecture",
    contribution:
      "Penalized by high-complexity functions, deep nesting, and God File findings.",
    formula:
      "100 - ((high_complexity * 2) + (deep_nesting * 3) + (god_files * 10))",
  },
  {
    score: "Testing",
    contribution:
      "Derived from architecture health with a small baseline penalty until dedicated test-coverage metrics are added.",
    formula: "architecture_score - 5",
  },
  {
    score: "Security",
    contribution:
      "Penalized by broad exception handling and empty exception blocks.",
    formula: "100 - ((broad_exception * 3) + (empty_exception * 5))",
  },
  {
    score: "Documentation",
    contribution:
      "Currently uses a deterministic baseline while documentation coverage analysis is on the roadmap.",
    formula: "85",
  },
  {
    score: "Scalability",
    contribution:
      "Penalized by the ratio of high-complexity functions to total functions.",
    formula: "100 - int((high_complexity / total_functions) * 500)",
  },
  {
    score: "Overall",
    contribution:
      "Summarizes repository maturity from the calculated score dimensions.",
    formula: "Average of the score dictionary after deterministic scores are calculated.",
  },
];

const exampleScores = [
  ["Architecture", 82],
  ["Testing", 77],
  ["Security", 91],
  ["Documentation", 85],
  ["Scalability", 96],
  ["Overall", 88],
] as const;

export default function HealthScoringPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Concepts"
        title="Health Scoring"
        description={
          <>
            RepoMind health scores are deterministic. They come from AST metrics,
            rule violations, repository structure, and explicit formulas rather
            than from an LLM response.
          </>
        }
      />

      <Section
        title="How Deterministic Metrics Contribute"
        description="The scanner collects source-code evidence, the rule engine converts metrics into findings, and the health engine applies penalties."
      >
        <div className="grid gap-4 md:grid-cols-2">
          {[
            "Cyclomatic complexity",
            "Maximum nesting depth",
            "Broad exception handling",
            "Empty exception handling",
            "God File findings",
            "Total parsed functions",
          ].map((metric) => (
            <div key={metric} className="rounded-lg border border-zinc-800 bg-zinc-900 p-4 text-sm text-zinc-300">
              {metric}
            </div>
          ))}
        </div>
      </Section>

      <Section title="Scores">
        <div className="space-y-4">
          {scoreRows.map((row) => (
            <div key={row.score} className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
              <h3 className="font-semibold text-zinc-100">{row.score}</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-400">
                {row.contribution}
              </p>
              <div className="mt-3 rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 font-mono text-xs text-indigo-300">
                {row.formula}
              </div>
            </div>
          ))}
        </div>
      </Section>

      <Section
        title="Example Scorecard"
        description="A typical analyze run prints each dimension and the overall maturity score."
      >
        <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
          <div className="space-y-5">
            {exampleScores.map(([label, value]) => (
              <ScoreBar key={label} label={label} value={value} />
            ))}
          </div>
        </div>
      </Section>

      <Callout title="AI does not assign health scores" variant="tip">
        AI can explain, prioritize, and plan from the findings, but the health
        score numbers are produced before AI synthesis begins.
      </Callout>
    </div>
  );
}
