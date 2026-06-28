import type { Metadata } from "next";
import {
  Brain,
  ClipboardList,
  FileText,
  GitBranch,
  Gauge,
  Layers,
  Route,
  ShieldCheck,
  Sparkles,
  Terminal,
} from "lucide-react";

import { Callout, PageHeader, Section, WorkflowFlow } from "@/components/docs";

export const metadata: Metadata = {
  title: "Workflow",
  description:
    "Visual RepoMind workflow from repository clone through AST analysis, rule engine, health scores, AI synthesis, recommendations, blueprints, and reports.",
};

const workflowSteps = [
  {
    title: "Repository",
    description: "Start with a GitHub repository URL.",
    icon: GitBranch,
  },
  {
    title: "Clone",
    description: "Validate the URL and clone or update the local repository cache.",
    icon: Terminal,
  },
  {
    title: "AST Analysis",
    description: "Parse supported source files and extract functions, imports, complexity, and nesting.",
    icon: Layers,
  },
  {
    title: "Rule Engine",
    description: "Evaluate deterministic findings using the selected JSON rule profile.",
    icon: ShieldCheck,
  },
  {
    title: "Health Scores",
    description: "Calculate architecture, testing, security, documentation, scalability, and overall scores.",
    icon: Gauge,
  },
  {
    title: "AI Issue Synthesis",
    description: "Send top deterministic findings to AI for issue synthesis and engineering context.",
    icon: Brain,
  },
  {
    title: "Recommendations",
    description: "Generate prioritized recommendations linked back to saved findings.",
    icon: Sparkles,
  },
  {
    title: "Blueprint",
    description: "Turn a recommendation ID into a concrete implementation plan.",
    icon: Route,
  },
  {
    title: "Report",
    description: "Export a Markdown report for team review and planning.",
    icon: FileText,
  },
];

export default function WorkflowPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Concepts"
        title="Workflow"
        description={
          <>
            RepoMind turns a repository URL into deterministic findings,
            persisted health intelligence, AI-assisted recommendations, and
            shareable implementation artifacts.
          </>
        }
      />

      <Section title="Visual Workflow">
        <WorkflowFlow steps={workflowSteps} />
      </Section>

      <Section title="Command Mapping">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <ClipboardList className="mb-3 h-6 w-6 text-indigo-400" />
            <h3 className="font-semibold text-zinc-100">Analyze</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Runs the full workflow through recommendations and saves state to
              PostgreSQL.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <ShieldCheck className="mb-3 h-6 w-6 text-indigo-400" />
            <h3 className="font-semibold text-zinc-100">Audit</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Stops after deterministic AST analysis and rule evaluation.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <Route className="mb-3 h-6 w-6 text-indigo-400" />
            <h3 className="font-semibold text-zinc-100">Blueprint</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Starts from a saved recommendation and generates an implementation
              plan.
            </p>
          </div>
          <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
            <FileText className="mb-3 h-6 w-6 text-indigo-400" />
            <h3 className="font-semibold text-zinc-100">Report</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Exports saved repository intelligence as Markdown.
            </p>
          </div>
        </div>
      </Section>

      <Callout title="Audit is intentionally shorter">
        Use audit when you want deterministic feedback only. Use analyze when
        you want RepoMind to carry the evidence into AI synthesis and planning.
      </Callout>
    </div>
  );
}
