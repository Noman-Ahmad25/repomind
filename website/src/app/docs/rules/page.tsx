import type { Metadata } from "next";

import { Callout, CodeBlock, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Rule Profiles",
  description:
    "Compare RepoMind's relaxed and strict deterministic rule profiles and learn when to use each one.",
};

const relaxedCommand =
  "docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json";

const strictCommand =
  "docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_strict.json";

const profileRows = [
  ["LOC warning / critical", "100 / 150", "30 / 50"],
  ["Nesting warning / critical", "5 / 7", "2 / 4"],
  ["Complexity warning / critical", "15 / 30", "8 / 15"],
  ["Parameters warning / critical", "6 / 10", "3 / 5"],
  ["File length critical", "2000", "500"],
  ["Broad exceptions", "BaseException", "Exception, BaseException, StandardError"],
  ["Empty exception bodies", "pass", "pass, return, continue"],
];

export default function RulesPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Guides"
        title="Rule Profiles"
        description={
          <>
            Rule profiles are JSON files that tune deterministic analysis
            thresholds. RepoMind ships with relaxed and strict profiles so teams
            can choose the right signal level for the moment.
          </>
        }
      />

      <Section
        title="rules_relaxed.json"
        description="Recommended for general repository analysis and early triage."
      >
        <div className="space-y-4">
          <p className="leading-7 text-zinc-400">
            The relaxed profile raises thresholds so RepoMind focuses on issues
            that are more likely to matter in everyday development. It is best
            for first runs, mature repositories with known complexity, and
            exploratory audits where you want fewer false positives.
          </p>
          <CodeBlock title="relaxed analysis" code={relaxedCommand} />
        </div>
      </Section>

      <Section
        title="rules_strict.json"
        description="Recommended for release-readiness, refactoring campaigns, and code-quality gates."
      >
        <div className="space-y-4">
          <p className="leading-7 text-zinc-400">
            The strict profile lowers thresholds and broadens pattern matching.
            It will surface more issues, which is useful when preparing a
            repository for production hardening or when you want to expose
            maintainability debt that relaxed analysis may ignore.
          </p>
          <CodeBlock title="strict analysis" code={strictCommand} />
        </div>
      </Section>

      <Section title="Profile Comparison">
        <div className="overflow-hidden rounded-lg border border-zinc-800">
          <table className="w-full text-left text-sm">
            <thead className="bg-zinc-900 text-zinc-300">
              <tr>
                <th className="px-4 py-3 font-semibold">Rule</th>
                <th className="px-4 py-3 font-semibold">Relaxed</th>
                <th className="px-4 py-3 font-semibold">Strict</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800">
              {profileRows.map(([label, relaxed, strict]) => (
                <tr key={label} className="bg-zinc-950/40">
                  <td className="px-4 py-3 text-zinc-300">{label}</td>
                  <td className="px-4 py-3 text-zinc-400">{relaxed}</td>
                  <td className="px-4 py-3 text-zinc-400">{strict}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="When to Use Each Profile">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <h3 className="font-semibold text-zinc-100">Use relaxed when</h3>
            <ul className="mt-3 space-y-2 text-sm leading-6 text-zinc-400">
              <li>You are analyzing a repository for the first time.</li>
              <li>You want a balanced signal-to-noise ratio.</li>
              <li>You are prioritizing the most obvious engineering debt.</li>
            </ul>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <h3 className="font-semibold text-zinc-100">Use strict when</h3>
            <ul className="mt-3 space-y-2 text-sm leading-6 text-zinc-400">
              <li>You are preparing for a production release.</li>
              <li>You want to catch smaller complexity and nesting issues.</li>
              <li>You are running a focused refactoring or hardening pass.</li>
            </ul>
          </div>
        </div>
      </Section>

      <Callout title="Profiles are versionable" variant="tip">
        Keep custom rule profiles in source control. That makes scoring changes
        explicit when thresholds evolve with the team.
      </Callout>
    </div>
  );
}
