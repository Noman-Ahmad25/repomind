
export default function QuickStartPage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-4xl font-bold tracking-tight text-white mb-4">
        Quick Start
      </h1>

      <p className="text-zinc-400 text-lg leading-relaxed">
        RepoMind provides four primary commands for repository analysis,
        deterministic auditing, engineering reporting, and implementation
        blueprint generation.
      </p>

      <div className="mt-8 space-y-10">
        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            Analyze a Repository
          </h2>

          <p className="text-zinc-400 mb-3">
            Run the complete engineering intelligence pipeline. RepoMind clones
            the repository, parses its architecture, generates (or reuses)
            embeddings, performs deterministic AST analysis, calculates
            evidence-based health scores, and produces AI-assisted engineering
            recommendations.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span>{" "}
            repomind analyze https://github.com/fastapi/fastapi
          </div>

          <div className="mt-6 rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
            <h3 className="text-zinc-100 font-semibold mb-4">
              Analysis Pipeline
            </h3>

            <pre className="text-sm text-zinc-400 leading-7 overflow-x-auto">
{`Git Repository
      │
      ▼
Repository Parsing
      │
      ▼
Embedding Generation / Cache
      │
      ▼
Deterministic AST Audit
      │
      ▼
Evidence-Based Health Scoring
      │
      ▼
AI Engineering Recommendations
      │
      ▼
Implementation Blueprints`}
            </pre>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            Deterministic Audit
          </h2>

          <p className="text-zinc-400 mb-3">
            Perform a fast, local-only AST audit without generating AI
            recommendations. This command identifies engineering issues directly
            from source code using deterministic analysis.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span>{" "}
            repomind audit https://github.com/fastapi/fastapi
          </div>

          <div className="mt-4 rounded-lg border border-zinc-800 bg-zinc-900/50 p-4">
            <h3 className="text-zinc-100 font-semibold mb-3">
              Detects
            </h3>

            <ul className="list-disc list-inside text-zinc-400 space-y-2">
              <li>High cyclomatic complexity</li>
              <li>Deep nesting</li>
              <li>Broad exception handling</li>
              <li>Empty exception blocks</li>
              <li>God Files</li>
              <li>Repository health metrics</li>
            </ul>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            Generate an Engineering Report
          </h2>

          <p className="text-zinc-400 mb-3">
            Export repository findings, health scores, and recommendations into
            a Markdown report suitable for sharing with your engineering team.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span>{" "}
            repomind report https://github.com/fastapi/fastapi
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            Generate an Implementation Blueprint
          </h2>

          <p className="text-zinc-400 mb-3">
            After running <code>analyze</code>, use the recommendation ID to
            generate a detailed implementation blueprint describing how to
            resolve the identified engineering issue.
          </p>

          <div className="bg-zinc-900 border border-zinc-800 rounded-md p-4 font-mono text-sm text-green-400 overflow-x-auto whitespace-nowrap">
            <span className="text-zinc-500">$</span>{" "}
            repomind blueprint &lt;recommendation_id&gt; --export
          </div>
        </section>
      </div>
    </div>
  );
}


