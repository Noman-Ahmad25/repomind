"use client";

import {
  Activity,
  BookOpen,
  Download,
  Gauge,
  HelpCircle,
  Map,
  Rocket,
  Route,
  ScrollText,
  Settings,
  Terminal,
  Workflow,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ComponentType } from "react";

import { docsNavGroups, type DocsIconName } from "@/lib/docs-nav";
import { cn } from "@/lib/utils";

const iconMap: Record<DocsIconName, ComponentType<{ className?: string }>> = {
  Activity,
  BookOpen,
  Download,
  Gauge,
  HelpCircle,
  Map,
  Rocket,
  Route,
  ScrollText,
  Settings,
  Terminal,
  Workflow,
};

export function DocsSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-full border-b border-zinc-800 py-6 md:w-72 md:border-b-0 md:border-r md:py-8 md:pr-8">
      <nav className="sticky top-24 space-y-7">
        {docsNavGroups.map((group) => (
          <div key={group.title}>
            <h4 className="mb-3 px-2 text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500">
              {group.title}
            </h4>
            <ul className="space-y-1 text-sm">
              {group.items.map((item) => {
                const Icon = iconMap[item.icon];
                const isActive = pathname === item.href;

                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={cn(
                        "flex items-center gap-2 rounded-md px-2 py-2 transition-colors",
                        isActive
                          ? "border border-indigo-500/20 bg-indigo-500/10 text-white"
                          : "text-zinc-400 hover:bg-zinc-900 hover:text-white",
                      )}
                    >
                      <Icon
                        className={cn(
                          "h-4 w-4",
                          isActive ? "text-indigo-400" : "text-zinc-500",
                        )}
                      />
                      <span>{item.title}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );
}
