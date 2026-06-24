export default function QuickStartPage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-4xl font-bold tracking-tight text-white mb-4">Quick Start</h1>
      <p className="text-zinc-400 text-lg leading-relaxed">
        Once installed, RepoMind AI operates through three primary commands: `analyze`, `report`, and `blueprint`.
      </p>

      <div className="mt-8 space-y-8">
        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">Step 1: Analyze a Repository</h2>
          <p className="text-zinc-400 mb-3">Feed any public GitHub URL to the intelligence engine. This will clone the code, parse the AST, generate semantic vectors, and calculate health scores.</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span> uv run repomind analyze https://github.com/fastapi/typer
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">Step 2: Generate a Report</h2>
          <p className="text-zinc-400 mb-3">Export the AI's findings into a highly readable Markdown document saved locally on your machine.</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span> uv run repomind report https://github.com/fastapi/typer
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">Step 3: Build a Blueprint</h2>
          <p className="text-zinc-400 mb-3">Copy the ID of any generated recommendation to create a step-by-step implementation plan.</p>
          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span> uv run repomind blueprint &lt;recommendation_id&gt; --export
          </div>
        </section>
      </div>
    </div>
  );
}