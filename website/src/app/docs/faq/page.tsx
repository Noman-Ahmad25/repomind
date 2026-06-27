import type { Metadata } from "next";

import { PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "FAQ",
  description:
    "Frequently asked questions about RepoMind deterministic analysis, AI synthesis, PostgreSQL, pgvector, rule profiles, and private repositories.",
};

const faqs = [
  {
    question: "Why deterministic analysis?",
    answer:
      "Deterministic analysis gives RepoMind repeatable evidence. Complexity, nesting, exception patterns, and repository structure can be recalculated the same way on every run, which makes scores and findings easier to trust.",
  },
  {
    question: "Why AI after static analysis?",
    answer:
      "AI is best used for synthesis and planning after facts are known. RepoMind first collects deterministic findings, then asks AI to explain impact, prioritize work, and produce implementation blueprints.",
  },
  {
    question: "Why PostgreSQL?",
    answer:
      "PostgreSQL gives RepoMind a durable local knowledge base for repositories, health scores, findings, recommendations, blueprints, and future query workflows.",
  },
  {
    question: "Why pgvector?",
    answer:
      "pgvector keeps semantic repository intelligence close to the relational data. That supports future semantic search, similarity lookups, and retrieval workflows without adding a separate vector database.",
  },
  {
    question: "Why two rule profiles?",
    answer:
      "Relaxed and strict profiles let teams choose signal level. Relaxed is better for first-pass analysis. Strict is better for release-readiness, hardening, and focused refactoring.",
  },
  {
    question: "Can private repositories be analyzed?",
    answer:
      "Yes, if the environment running RepoMind can clone the repository. Configure Git credentials or tokens in the shell or container environment before running analyze or audit.",
  },
  {
    question: "Does RepoMind execute application code?",
    answer:
      "No. RepoMind clones source code and parses it statically. The scanner does not run the target repository's application code.",
  },
  {
    question: "Do reports require a previous analysis?",
    answer:
      "Yes. The report command reads saved health scores, findings, and recommendations from PostgreSQL, so run analyze before exporting a report.",
  },
];

export default function FAQPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Reference"
        title="FAQ"
        description={
          <>
            Common questions about how RepoMind analyzes repositories, stores
            intelligence, and uses AI.
          </>
        }
      />

      <Section title="Questions">
        <div className="space-y-4">
          {faqs.map((faq) => (
            <div key={faq.question} className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
              <h3 className="font-semibold text-zinc-100">{faq.question}</h3>
              <p className="mt-2 text-sm leading-6 text-zinc-400">
                {faq.answer}
              </p>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
