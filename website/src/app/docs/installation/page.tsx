import type { Metadata } from "next";

import { Callout, CodeBlock, PageHeader, Section } from "@/components/docs";

export const metadata: Metadata = {
  title: "Installation",
  description:
    "Install RepoMind with the recommended Docker Compose workflow or a manual Python and PostgreSQL setup.",
};

const cloneCommands = `git clone https://github.com/Noman-Ahmad25/repomind.git
cd repomind`;

const envDocker = `GEMINI_API_KEY=your_gemini_api_key`;

const dockerStart = `docker compose up -d app`;

const dockerMigrate = `docker compose exec app alembic upgrade head`;

const dockerVerify = `docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json`;

const dockerAudit = `docker compose exec app repomind audit https://github.com/fastapi/fastapi --rules rules_relaxed.json`;

const envLocal = `GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/repomind`;

const localInstall = `uv sync
uv run alembic upgrade head`;

const localVerify = `uv run repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json`;

export default function InstallationPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="Getting Started"
        title="Installation"
        description={
          <>
            Docker Compose is the recommended way to run RepoMind because it
            starts the CLI environment and the PostgreSQL + pgvector knowledge
            store with one workflow.
          </>
        }
      />

      <Callout title="Recommended path" variant="tip">
        Use Docker first unless you are actively developing RepoMind itself. The
        Compose setup wires the app container to the database using the service
        hostname <code className="text-zinc-100">db</code>.
      </Callout>

      <Section
        title="Docker Installation"
        description="Start here for the most repeatable setup."
      >
        <div className="space-y-6">
          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              1. Clone RepoMind
            </h3>
            <CodeBlock title="clone" code={cloneCommands} />
          </div>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              2. Configure Gemini
            </h3>
            <p className="mb-3 text-zinc-400">
              Create a <code className="text-zinc-200">.env</code> file in the
              project root. Docker provides the container database URL from
              <code className="text-zinc-200"> docker-compose.yml</code>.
            </p>
            <CodeBlock title=".env" code={envDocker} language="env" />
          </div>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              3. Start the app service
            </h3>
            <CodeBlock title="docker" code={dockerStart} />
          </div>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              4. Run migrations
            </h3>
            <p className="mb-3 text-zinc-400">
              Create the repository, health, findings, recommendations, and
              blueprint tables before the first analysis.
            </p>
            <CodeBlock title="database" code={dockerMigrate} />
          </div>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              5. Verify the installation
            </h3>
            <CodeBlock title="analyze" code={dockerVerify} />
          </div>

          <Callout title="Run commands inside the container">
            Prefix CLI commands with{" "}
            <code className="text-zinc-100">docker compose exec app</code> when
            using Docker. For example:
          </Callout>

          <CodeBlock title="audit" code={dockerAudit} />
        </div>
      </Section>

      <Section
        title="Docker Configuration"
        description="The Compose file defines a PostgreSQL 16 database with pgvector and an app service that mounts the repository."
      >
        <div className="overflow-hidden rounded-lg border border-zinc-800">
          <div className="grid grid-cols-2 gap-px bg-zinc-800 text-sm">
            {[
              ["Database image", "pgvector/pgvector:pg16"],
              ["Database name", "repomind"],
              ["Username", "postgres"],
              ["Password", "password"],
              ["Host port", "5432"],
              [
                "Container DATABASE_URL",
                "postgresql+psycopg://postgres:password@db:5432/repomind",
              ],
            ].map(([label, value]) => (
              <div key={label} className="contents">
                <div className="bg-zinc-900 px-4 py-3 text-zinc-500">
                  {label}
                </div>
                <div className="bg-zinc-900 px-4 py-3 text-zinc-200">
                  {value}
                </div>
              </div>
            ))}
          </div>
        </div>
      </Section>

      <Section
        title="Manual Installation"
        description="Use this setup when you want to run the CLI directly on your host machine."
      >
        <div className="space-y-6">
          <Callout title="Manual prerequisites" variant="warning">
            Manual mode requires Python 3.12+, uv, Git, PostgreSQL with pgvector,
            and a reachable database URL.
          </Callout>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              1. Install dependencies and run migrations
            </h3>
            <CodeBlock title="local setup" code={localInstall} />
          </div>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              2. Configure environment variables
            </h3>
            <CodeBlock title=".env" code={envLocal} language="env" />
          </div>

          <div>
            <h3 className="mb-3 font-semibold text-zinc-100">
              3. Run RepoMind locally
            </h3>
            <CodeBlock title="analyze" code={localVerify} />
          </div>
        </div>
      </Section>
    </div>
  );
}
