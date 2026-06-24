export default function InstallationPage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-4xl font-bold tracking-tight text-white mb-4">Installation</h1>
      <p className="text-zinc-400 text-lg leading-relaxed">
        RepoMind AI requires Python 3.12, Docker (for the PostgreSQL database), and the `uv` package manager.
      </p>

      <div className="mt-8 space-y-8">
        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">1. Clone the Repository</h2>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            git clone https://github.com/yourusername/repomind.git<br/>
            cd repomind
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">2. Start the Database</h2>
          <p className="text-zinc-400 mb-3">Spin up the PostgreSQL database with the pgvector extension using Docker Compose:</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            docker compose up -d
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">3. Install Dependencies</h2>
          <p className="text-zinc-400 mb-3">Use `uv` to sync the environment and apply the database migrations:</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            uv sync<br/>
            uv run alembic upgrade head
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">4. Configure Environment</h2>
          <p className="text-zinc-400 mb-3">Create a `.env` file in the root directory and add your Gemini API key:</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-zinc-300">
            GEMINI_API_KEY=your_api_key_here
          </div>
        </section>
      </div>
    </div>
  );
}