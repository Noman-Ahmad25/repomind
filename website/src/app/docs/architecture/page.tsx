import type { Metadata } from "next";
import {
  Brain,
  Database,
  FileText,
  GitBranch,
  Gauge,
  Layers,
  Route,
  ShieldCheck,
  Sparkles,
  Terminal,
} from "lucide-react";

import {
  Callout,
  FeatureCard,
  PageHeader,
  Section,
  WorkflowFlow,
} from "@/components/docs";

export const metadata: Metadata = {
  title: "Architecture",
  description:
    "RepoMind architecture from repository clone through AST analysis, rule evaluation, health scoring, PostgreSQL, AI recommendations, blueprints, and reports.",
};

const architectureSteps = [
  {
    title: "Repository",
    description: "A public or private GitHub repository URL is the pipeline input.",
    icon: GitBranch,
  },
  {
    title: "Clone",
    description:
      "RepoMind validates the GitHub URL, clones the repository, and caches it under repositories/.",
    icon: Terminal,
  },
  {
    title: "AST Engine",
    description:
      "The scanner routes supported files to deterministic analyzers and extracts structure without executing project code.",
    icon: Layers,
  },
  {
    title: "Rule Engine",
    description:
      "Rule profiles evaluate complexity, nesting, exception handling, unused imports, and large-file signals.",
    icon: ShieldCheck,
  },
  {
    title: "Health Score Engine",
    description:
      "Architecture, testing, security, documentation, scalability, and overall scores are calculated from metrics.",
    icon: Gauge,
  },
  {
    title: "PostgreSQL",
    description:
      "Repository metadata, health reports, findings, recommendations, blueprints, and vector data are persisted locally.",
    icon: Database,
  },
  {
    title: "AI Layer",
    description:
      "Gemini synthesizes engineering issues and plans only after deterministic evidence exists.",
    icon: Brain,
  },
  {
    title: "Recommendations",
    description:
      "RepoMind ranks engineering actions by priority, impact, effort, and linked findings.",
    icon: Sparkles,
  },
  {
    title: "Blueprints",
    description:
      "A recommendation ID can become a concrete implementation plan for code changes.",
    icon: Route,
  },
  {
    title: "Reports",
    description:
      "Markdown exports capture health, findings, recommendations, and blueprint artifacts.",
    icon: FileText,
  },
];

export default function ArchitecturePage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Concepts"
        title="System Architecture"
        description={
          <>
            RepoMind follows an evidence-first architecture. Deterministic
            metrics are collected before AI is used for issue synthesis,
            prioritization, and implementation planning.
          </>
        }
      />

      <Section
        title="End-to-End Pipeline"
        description="The architecture moves from source evidence to persisted intelligence and shareable outputs."
      >
        <WorkflowFlow steps={architectureSteps} />
      </Section>

      <Section title="Core Layers">
        <div className="grid gap-4 md:grid-cols-2">
          <FeatureCard icon={GitBranch} title="Repository Layer">
            Validates GitHub URLs, clones repositories, updates cached working
            copies, and records owner/name metadata for downstream reporting.
          </FeatureCard>
          <FeatureCard icon={Layers} title="Deterministic Analysis Layer">
            Performs single-pass scanning and Python AST analysis for functions,
            imports, complexity, nesting, and exception-handling patterns.
          </FeatureCard>
          <FeatureCard icon={Database} title="Knowledge Layer">
            Stores repositories, health scores, findings, recommendations,
            blueprints, and vector-ready repository intelligence in PostgreSQL.
          </FeatureCard>
          <FeatureCard icon={Brain} title="AI Engineering Layer">
            Uses deterministic findings as input to generate issue summaries,
            prioritized recommendations, and implementation blueprints.
          </FeatureCard>
        </div>
      </Section>

      <Section title="Design Principles">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <h3 className="font-semibold text-zinc-100">Evidence First</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Static analysis and rule evaluation happen before AI reasoning.
              Recommendations are grounded in collected repository evidence.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <h3 className="font-semibold text-zinc-100">Local by Default</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              The repository cache, deterministic analysis, database, reports,
              and blueprint exports all run from the developer environment.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <h3 className="font-semibold text-zinc-100">Repeatable Scoring</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Health scores are mathematical outputs from the same metrics and
              rule profile, making runs comparable over time.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <h3 className="font-semibold text-zinc-100">AI After Analysis</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              AI is used for synthesis, prioritization, and planning rather than
              as the primary source of static-analysis truth.
            </p>
          </div>
        </div>
      </Section>

      <Callout title="Why PostgreSQL sits before AI">
        RepoMind persists repository evidence before synthesis so reports,
        recommendations, and blueprints can be traced back to saved findings
        instead of a one-off prompt response.
      </Callout>
    </div>
  );
}
