import type { Metadata } from "next";
import {
  Bot,
  Code2,
  GitBranch,
  GitPullRequest,
  Puzzle,
  Search,
  Wand2,
} from "lucide-react";

import { FeatureCard, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Roadmap",
  description:
    "RepoMind roadmap for multi-language support, incremental analysis, semantic search, GitHub App, VSCode Extension, automatic code generation, and agentic workflows.",
};

const roadmap = [
  {
    title: "Multi-language support",
    icon: Code2,
    description:
      "Expand the routed analyzer architecture beyond Python into additional production languages and frameworks.",
  },
  {
    title: "Incremental analysis",
    icon: GitPullRequest,
    description:
      "Analyze changed files and changed functions so repository intelligence updates quickly between commits.",
  },
  {
    title: "Semantic search",
    icon: Search,
    description:
      "Use persisted embeddings and pgvector to search repository concepts, patterns, and historical findings.",
  },
  {
    title: "GitHub App",
    icon: GitBranch,
    description:
      "Bring RepoMind analysis into pull requests, repository dashboards, and team workflows.",
  },
  {
    title: "VSCode Extension",
    icon: Puzzle,
    description:
      "Surface repository health, findings, recommendations, and blueprints directly inside the editor.",
  },
  {
    title: "Automatic code generation",
    icon: Wand2,
    description:
      "Turn approved blueprints into generated patches with tests and reviewable implementation steps.",
  },
  {
    title: "Agentic engineering workflows",
    icon: Bot,
    description:
      "Coordinate analysis, planning, implementation, verification, and reporting across engineering agents.",
  },
];

export default function RoadmapPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Reference"
        title="Roadmap"
        description={
          <>
            RepoMind is moving from repository intelligence into full
            engineering workflow orchestration while preserving its
            evidence-first foundation.
          </>
        }
      />

      <Section title="Planned Capabilities">
        <div className="grid gap-4 md:grid-cols-2">
          {roadmap.map((item) => (
            <FeatureCard key={item.title} icon={item.icon} title={item.title}>
              {item.description}
            </FeatureCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
