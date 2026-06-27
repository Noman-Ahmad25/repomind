import type { Metadata } from "next";

import { Callout, CodeBlock, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Configuration",
  description:
    "Configure RepoMind with GEMINI_API_KEY, DATABASE_URL, Docker Compose, and local environment settings.",
};

const dockerEnv = `GEMINI_API_KEY=your_gemini_api_key`;

const localEnv = `GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/repomind`;

const dockerCommands = `docker compose up -d app
docker compose exec app alembic upgrade head
docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json`;

const localCommands = `uv sync
uv run alembic upgrade head
uv run repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json`;

export default function ConfigurationPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Guides"
        title="Configuration"
        description={
          <>
            RepoMind needs an AI API key for synthesis and a PostgreSQL database
            for persistent repository intelligence.
          </>
        }
      />

      <Section title="Environment Variables">
        <div className="overflow-hidden rounded-lg border border-zinc-800">
          <div className="divide-y divide-zinc-800">
            <div className="grid gap-2 bg-zinc-900 p-4 sm:grid-cols-[180px_1fr]">
              <code className="font-mono text-sm text-indigo-300">
                GEMINI_API_KEY
              </code>
              <p className="text-sm leading-6 text-zinc-400">
                Required for AI issue synthesis, recommendation generation, and
                blueprint generation. The deterministic audit can run without
                AI, but analyze and blueprint need this value.
              </p>
            </div>
            <div className="grid gap-2 bg-zinc-900 p-4 sm:grid-cols-[180px_1fr]">
              <code className="font-mono text-sm text-indigo-300">
                DATABASE_URL
              </code>
              <p className="text-sm leading-6 text-zinc-400">
                SQLAlchemy database URL for PostgreSQL. Local mode defaults to
                postgresql+psycopg://postgres:password@localhost:5432/repomind
                when the variable is not set.
              </p>
            </div>
          </div>
        </div>
      </Section>

      <Section
        title="Docker Configuration"
        description="Docker is the recommended configuration because Compose provides the database service and app environment."
      >
        <div className="space-y-5">
          <p className="leading-7 text-zinc-400">
            In Docker mode, keep your Gemini key in a root{" "}
            <code className="text-zinc-200">.env</code> file. The app service
            gets its database URL from <code className="text-zinc-200">docker-compose.yml</code>
            and connects to PostgreSQL through the internal service name{" "}
            <code className="text-zinc-200">db</code>.
          </p>
          <CodeBlock title=".env" code={dockerEnv} language="env" />
          <CodeBlock title="docker workflow" code={dockerCommands} />
        </div>
      </Section>

      <Section
        title="Local Configuration"
        description="Local mode runs the CLI on your host machine and connects to a reachable PostgreSQL instance."
      >
        <div className="space-y-5">
          <CodeBlock title=".env" code={localEnv} language="env" />
          <CodeBlock title="local workflow" code={localCommands} />
          <Callout title="Database hostnames differ" variant="warning">
            Use <code className="text-zinc-100">db</code> only inside Docker
            Compose. Use <code className="text-zinc-100">localhost</code> when
            the CLI runs on your host and PostgreSQL is exposed on port 5432.
          </Callout>
        </div>
      </Section>

      <Section title="Configuration Checklist">
        <div className="grid gap-4 md:grid-cols-2">
          {[
            "The .env file exists in the repository root.",
            "GEMINI_API_KEY is set before running analyze or blueprint.",
            "PostgreSQL is running with the repomind database.",
            "Alembic migrations have been applied.",
          ].map((item) => (
            <div key={item} className="rounded-lg border border-zinc-800 bg-zinc-900 p-4 text-sm text-zinc-300">
              {item}
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
