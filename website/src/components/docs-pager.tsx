"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { getAdjacentDocs } from "@/lib/docs-nav";

export function DocsPager() {
  const pathname = usePathname();
  const { previous, next } = getAdjacentDocs(pathname);

  if (!previous && !next) {
    return null;
  }

  return (
    <nav className="mt-14 grid gap-3 border-t border-zinc-800 pt-6 sm:grid-cols-2">
      {previous ? (
        <Link
          href={previous.href}
          className="group rounded-lg border border-zinc-800 bg-zinc-900/50 p-4 transition hover:border-zinc-700 hover:bg-zinc-900"
        >
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-[0.14em] text-zinc-500">
            <ChevronLeft className="h-3.5 w-3.5 transition group-hover:-translate-x-0.5" />
            Previous
          </div>
          <div className="mt-2 font-semibold text-zinc-100">
            {previous.title}
          </div>
          <p className="mt-1 text-sm text-zinc-500">{previous.description}</p>
        </Link>
      ) : (
        <div />
      )}

      {next ? (
        <Link
          href={next.href}
          className="group rounded-lg border border-zinc-800 bg-zinc-900/50 p-4 text-left transition hover:border-zinc-700 hover:bg-zinc-900 sm:text-right"
        >
          <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-[0.14em] text-zinc-500 sm:justify-end">
            Next
            <ChevronRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
          </div>
          <div className="mt-2 font-semibold text-zinc-100">{next.title}</div>
          <p className="mt-1 text-sm text-zinc-500">{next.description}</p>
        </Link>
      ) : null}
    </nav>
  );
}
