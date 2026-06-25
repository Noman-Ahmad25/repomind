export default function ArchitecturePage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-4xl font-bold tracking-tight text-white mb-4">
        System Architecture
      </h1>

      <p className="text-zinc-400 text-lg leading-relaxed">
        RepoMind follows an <strong className="text-zinc-200">evidence-first architecture</strong>.
        Repository metrics are gathered through deterministic static analysis before
        AI is used to synthesize engineering recommendations and implementation
        blueprints.
      </p>

      <section className="mt-8 rounded-xl border border-zinc-800 bg-zinc-900 p-6 overflow-x-auto">
        <pre className="text-sm text-zinc-300 leading-7">
{`                    Git Repository
                           │
                           ▼
                  Repository Loader
                           │
                           ▼
                  Repository Parser
                           │
                           ▼
               Deterministic AST Engine
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
 Complexity Analysis   Security Analysis   God File Detection
      │                    │                    │
      └────────────────────┼────────────────────┘
                           │
                           ▼
           Evidence-Based Health Scoring
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        PostgreSQL Metadata     pgvector Embeddings
             (Docker)               (Docker)
                │                     │
                └──────────┬──────────┘
                           ▼
             AI Engineering Intelligence
                           │
                           ▼
          Recommendations & Blueprints`}
        </pre>
      </section>

      <div className="mt-10 space-y-10">

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            1. Repository Layer
          </h2>

          <p className="text-zinc-400 mb-4">
            RepoMind begins by cloning the target repository and extracting
            structural metadata without executing application code.
          </p>

          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li>
              <strong className="text-zinc-200">GitPython</strong> clones and
              manages repositories.
            </li>
            <li>
              Repository metadata including files, classes, and functions is
              collected for further analysis.
            </li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            2. Deterministic Analysis Engine
          </h2>

          <p className="text-zinc-400 mb-4">
            RepoMind performs deterministic static analysis using Python AST.
            Engineering metrics are calculated locally without relying on AI.
          </p>

          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li>Cyclomatic complexity analysis</li>
            <li>Nesting depth analysis</li>
            <li>Broad exception detection</li>
            <li>Empty exception detection</li>
            <li>God File detection</li>
            <li>Repository health scoring</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            3. Knowledge Layer
          </h2>

          <p className="text-zinc-400 mb-4">
            Repository intelligence is persisted locally using Dockerized
            PostgreSQL with the pgvector extension.
          </p>

          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li>Repository metadata</li>
            <li>Health reports</li>
            <li>Engineering findings</li>
            <li>Semantic vector embeddings</li>
            <li>Recommendation history</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            4. AI Engineering Intelligence
          </h2>

          <p className="text-zinc-400 mb-4">
            AI is applied only after deterministic analysis has produced
            evidence-backed findings.
          </p>

          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li>Repository maturity classification</li>
            <li>Engineering recommendation generation</li>
            <li>Implementation blueprint generation</li>
            <li>Structured JSON responses validated using Pydantic</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold text-zinc-100 mb-4 border-b border-zinc-800 pb-2">
            Design Principles
          </h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
              <h3 className="font-semibold text-zinc-100 mb-2">
                Evidence First
              </h3>
              <p className="text-sm text-zinc-400">
                Repository metrics are produced through deterministic analysis
                before AI reasoning begins.
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
              <h3 className="font-semibold text-zinc-100 mb-2">
                Local by Default
              </h3>
              <p className="text-sm text-zinc-400">
                Static analysis, vector generation, and database storage all run
                locally.
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
              <h3 className="font-semibold text-zinc-100 mb-2">
                Deterministic
              </h3>
              <p className="text-sm text-zinc-400">
                Health scores are computed mathematically rather than generated
                by an LLM.
              </p>
            </div>

            <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
              <h3 className="font-semibold text-zinc-100 mb-2">
                AI-Assisted
              </h3>
              <p className="text-sm text-zinc-400">
                AI focuses on engineering reasoning, prioritization, and
                blueprint generation instead of static code analysis.
              </p>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}