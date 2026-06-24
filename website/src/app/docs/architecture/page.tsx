export default function ArchitecturePage() {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h1 className="text-4xl font-bold tracking-tight text-white mb-4">System Architecture</h1>
      <p className="text-zinc-400 text-lg leading-relaxed">
        RepoMind AI relies on a heavily decoupled architecture combining local machine learning with remote LLM reasoning.
      </p>

      <div className="mt-8 space-y-8">
        <section>
          <h2 className="text-xl font-semibold text-zinc-100 mb-3">1. The Extraction Layer</h2>
          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li><strong className="text-zinc-200">GitPython:</strong> Handles raw repository cloning and version control metadata.</li>
            <li><strong className="text-zinc-200">Tree-Sitter:</strong> Generates Abstract Syntax Trees (ASTs) to physically count classes, functions, and files without executing the code.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-zinc-100 mb-3">2. The Knowledge Layer</h2>
          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li><strong className="text-zinc-200">Sentence Transformers:</strong> Runs a small BGE model locally to generate semantic embeddings.</li>
            <li><strong className="text-zinc-200">PostgreSQL + pgvector:</strong> Provides enterprise-grade vector storage and rapid similarity search capabilities.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold text-zinc-100 mb-3">3. The Intelligence Layer</h2>
          <ul className="list-disc list-inside text-zinc-400 space-y-2 ml-4">
            <li><strong className="text-zinc-200">Gemini Models:</strong> Processes architectural metrics to detect maturity stages, audit technical debt, and invent missing capabilities.</li>
            <li><strong className="text-zinc-200">Pydantic & JSON:</strong> Enforces strict schema validation for all LLM outputs to guarantee terminal readability.</li>
          </ul>
        </section>
      </div>
    </div>
  );
}