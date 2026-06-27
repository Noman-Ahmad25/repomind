"use client";

import { Check, Copy } from "lucide-react";
import { useState } from "react";

import { cn } from "@/lib/utils";

type CopyButtonProps = {
  value: string;
  className?: string;
};

export function CopyButton({ value, className }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(value);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }

  const Icon = copied ? Check : Copy;

  return (
    <button
      type="button"
      onClick={handleCopy}
      className={cn(
        "inline-flex h-8 items-center gap-2 rounded-md border border-zinc-700 bg-zinc-950/80 px-2.5 text-xs font-medium text-zinc-300 shadow-sm transition hover:border-zinc-600 hover:bg-zinc-900 hover:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50",
        className,
      )}
      aria-label={copied ? "Copied command" : "Copy command"}
    >
      <Icon className="h-3.5 w-3.5" />
      <span className="hidden sm:inline">{copied ? "Copied" : "Copy"}</span>
    </button>
  );
}
