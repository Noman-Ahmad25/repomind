import {
  AlertTriangle,
  ArrowDown,
  CheckCircle2,
  Info,
  Lightbulb,
} from "lucide-react";
import type { ComponentType, ReactNode } from "react";

import { CopyButton } from "@/components/copy-button";
import { cn } from "@/lib/utils";

type IconComponent = ComponentType<{ className?: string }>;

export function PageHeader({
  eyebrow,
  title,
  description,
}: {
  eyebrow?: string;
  title: string;
  description: ReactNode;
}) {
  return (
    <header className="space-y-4">
      {eyebrow ? (
        <div className="text-sm font-medium text-indigo-400">{eyebrow}</div>
      ) : null}
      <h1 className="text-4xl font-bold tracking-tight text-white">{title}</h1>
      <p className="max-w-3xl text-lg leading-relaxed text-zinc-400">
        {description}
      </p>
    </header>
  );
}

export function Section({
  title,
  description,
  children,
}: {
  title: string;
  description?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="space-y-4">
      <div className="border-b border-zinc-800 pb-3">
        <h2 className="text-2xl font-semibold text-zinc-100">{title}</h2>
        {description ? (
          <p className="mt-2 max-w-3xl text-zinc-400">{description}</p>
        ) : null}
      </div>
      {children}
    </section>
  );
}

export function CodeBlock({
  code,
  title,
  language = "bash",
  className,
}: {
  code: string;
  title?: string;
  language?: string;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-lg border border-zinc-800 bg-zinc-950",
        className,
      )}
    >
      {title ? (
        <div className="flex items-center justify-between gap-3 border-b border-zinc-800 bg-zinc-900/70 px-4 py-2.5">
          <span className="font-mono text-xs text-zinc-500">{title}</span>
          <CopyButton value={code} />
        </div>
      ) : (
        <CopyButton value={code} className="absolute right-3 top-3 z-10" />
      )}
      <pre className="overflow-x-auto p-4 pr-24 text-sm leading-7 text-zinc-300">
        <code data-language={language}>{code}</code>
      </pre>
    </div>
  );
}

export function Callout({
  title,
  children,
  variant = "info",
}: {
  title: string;
  children: ReactNode;
  variant?: "info" | "tip" | "warning";
}) {
  const Icon =
    variant === "warning" ? AlertTriangle : variant === "tip" ? Lightbulb : Info;
  const tone =
    variant === "warning"
      ? "border-yellow-500/20 bg-yellow-500/5 text-yellow-300"
      : variant === "tip"
        ? "border-emerald-500/20 bg-emerald-500/5 text-emerald-300"
        : "border-indigo-500/20 bg-indigo-500/5 text-indigo-300";

  return (
    <div className={cn("rounded-lg border p-4", tone)}>
      <div className="flex items-start gap-3">
        <Icon className="mt-0.5 h-4 w-4 shrink-0" />
        <div>
          <h3 className="font-semibold text-zinc-100">{title}</h3>
          <div className="mt-1 text-sm leading-6 text-zinc-300">{children}</div>
        </div>
      </div>
    </div>
  );
}

export function FeatureCard({
  icon: Icon,
  title,
  children,
}: {
  icon: IconComponent;
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-5">
      <Icon className="mb-4 h-7 w-7 text-indigo-400" />
      <h3 className="font-semibold text-zinc-100">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-zinc-400">{children}</p>
    </div>
  );
}

export function StatCard({
  value,
  label,
  description,
}: {
  value: string;
  label: string;
  description: string;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/70 p-5">
      <div className="text-3xl font-bold tracking-tight text-white">{value}</div>
      <div className="mt-1 font-medium text-zinc-200">{label}</div>
      <p className="mt-2 text-sm leading-6 text-zinc-500">{description}</p>
    </div>
  );
}

export function WorkflowFlow({
  steps,
}: {
  steps: {
    title: string;
    description: string;
    icon?: IconComponent;
  }[];
}) {
  return (
    <div className="space-y-3">
      {steps.map((step, index) => {
        const Icon = step.icon ?? CheckCircle2;

        return (
          <div key={step.title}>
            <div className="flex items-start gap-4 rounded-lg border border-zinc-800 bg-zinc-900 p-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-indigo-500/20 bg-indigo-500/10">
                <Icon className="h-5 w-5 text-indigo-400" />
              </div>
              <div>
                <h3 className="font-semibold text-zinc-100">{step.title}</h3>
                <p className="mt-1 text-sm leading-6 text-zinc-400">
                  {step.description}
                </p>
              </div>
            </div>
            {index < steps.length - 1 ? (
              <div className="flex justify-center py-2 text-zinc-600">
                <ArrowDown className="h-5 w-5" />
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}

export function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between text-sm">
        <span className="font-medium text-zinc-300">{label}</span>
        <span className="font-mono text-zinc-400">{value}/100</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-zinc-800">
        <div
          className="h-full rounded-full bg-indigo-500"
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}
