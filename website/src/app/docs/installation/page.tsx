
export default function InstallationPage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-4xl font-bold tracking-tight text-white mb-4">
        Installation
      </h1>

      <p className="text-zinc-400 text-lg leading-relaxed">
        RepoMind requires <strong className="text-zinc-200">Python 3.12+</strong>,
        <strong className="text-zinc-200"> Docker</strong> (for PostgreSQL +
        pgvector), and the <code>uv</code> package manager.
      </p>

      <div className="mt-8 space-y-10">
        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            1. Clone the Repository
          </h2>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300 overflow-x-auto">
            git clone https://github.com/yourusername/repomind.git
            <br />
            cd repomind
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            2. Install Dependencies
          </h2>

          <p className="text-zinc-400 mb-3">
            Install all project dependencies using{" "}
            <code className="text-zinc-200">uv</code>.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            uv sync
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            3. Start PostgreSQL
          </h2>

          <p className="text-zinc-400 mb-3">
            RepoMind uses PostgreSQL 16 with the pgvector extension running inside
            Docker. Start the database with:
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            docker compose up -d
          </div>

          <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-900/50 p-4">
            <h3 className="text-zinc-100 font-semibold mb-3">
              Default Database Configuration
            </h3>

            <div className="grid grid-cols-2 gap-y-2 text-sm">
              <span className="text-zinc-500">Image</span>
              <span className="text-zinc-200">
                pgvector/pgvector:pg16
              </span>

              <span className="text-zinc-500">Database</span>
              <span className="text-zinc-200">repomind</span>

              <span className="text-zinc-500">Username</span>
              <span className="text-zinc-200">postgres</span>

              <span className="text-zinc-500">Password</span>
              <span className="text-zinc-200">password</span>

              <span className="text-zinc-500">Port</span>
              <span className="text-zinc-200">5432</span>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            4. Run Database Migrations
          </h2>

          <p className="text-zinc-400 mb-3">
            Create the required database schema.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            uv run alembic upgrade head
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            5. Configure Environment
          </h2>

          <p className="text-zinc-400 mb-3">
            Create a <code>.env</code> file and add your Gemini API key.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            GEMINI_API_KEY=your_api_key
          </div>

          <div className="mt-4 rounded-lg border border-indigo-500/20 bg-indigo-500/5 p-4">
            <p className="text-sm text-zinc-300">
              <strong className="text-white">Note:</strong> Docker starts the
              PostgreSQL database automatically. RepoMind connects to the running
              database using the project's configuration, so no additional Docker
              setup is required after the container is running.
            </p>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            6. Verify Installation
          </h2>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400">
            uv run repomind analyze https://github.com/fastapi/fastapi
          </div>
        </section>
      </div>
    </div>
  );
}
