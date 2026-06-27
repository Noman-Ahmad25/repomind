export type DocsIconName =
  | "Activity"
  | "BookOpen"
  | "Download"
  | "Gauge"
  | "HelpCircle"
  | "Map"
  | "Rocket"
  | "Route"
  | "ScrollText"
  | "Settings"
  | "Terminal"
  | "Workflow";

export type DocsNavItem = {
  title: string;
  href: string;
  description: string;
  icon: DocsIconName;
};

export type DocsNavGroup = {
  title: string;
  items: DocsNavItem[];
};

export const docsNavGroups: DocsNavGroup[] = [
  {
    title: "Getting Started",
    items: [
      {
        title: "Installation",
        href: "/docs/installation",
        description: "Install RepoMind with Docker or a local Python setup.",
        icon: "Download",
      },
      {
        title: "Quick Start",
        href: "/docs/quick-start",
        description: "Run analyze, audit, report, and blueprint commands.",
        icon: "Rocket",
      },
    ],
  },
  {
    title: "Guides",
    items: [
      {
        title: "Commands",
        href: "/docs/commands",
        description: "Every CLI command, argument, output, and note.",
        icon: "Terminal",
      },
      {
        title: "Rule Profiles",
        href: "/docs/rules",
        description: "Relaxed and strict deterministic analysis profiles.",
        icon: "ScrollText",
      },
      {
        title: "Configuration",
        href: "/docs/configuration",
        description: "Environment variables, Docker, and local settings.",
        icon: "Settings",
      },
    ],
  },
  {
    title: "Concepts",
    items: [
      {
        title: "Workflow",
        href: "/docs/workflow",
        description: "The repository intelligence pipeline from clone to report.",
        icon: "Workflow",
      },
      {
        title: "Architecture",
        href: "/docs/architecture",
        description: "How deterministic analysis, storage, and AI fit together.",
        icon: "Route",
      },
      {
        title: "Health Scoring",
        href: "/docs/health-scoring",
        description: "How RepoMind computes health scores from evidence.",
        icon: "Gauge",
      },
    ],
  },
  {
    title: "Reference",
    items: [
      {
        title: "Examples",
        href: "/docs/examples",
        description: "Complete workflows with expected outputs.",
        icon: "BookOpen",
      },
      {
        title: "FAQ",
        href: "/docs/faq",
        description: "Common questions about RepoMind design choices.",
        icon: "HelpCircle",
      },
      {
        title: "Roadmap",
        href: "/docs/roadmap",
        description: "Planned platform and workflow capabilities.",
        icon: "Map",
      },
    ],
  },
];

export const docsNavItems = docsNavGroups.flatMap((group) => group.items);

export function getDocByHref(pathname: string) {
  return docsNavItems.find((item) => item.href === pathname);
}

export function getAdjacentDocs(pathname: string) {
  const index = docsNavItems.findIndex((item) => item.href === pathname);

  if (index === -1) {
    return { previous: undefined, next: docsNavItems[0] };
  }

  return {
    previous: docsNavItems[index - 1],
    next: docsNavItems[index + 1],
  };
}
