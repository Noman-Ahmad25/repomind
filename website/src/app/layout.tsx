
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://repomind.dev"),
  applicationName: "RepoMind",

  title: {
    default: "RepoMind - Repository Intelligence",
    template: "%s | RepoMind",
  },

  description:
    "Evidence-driven repository intelligence platform combining deterministic AST analysis with AI-assisted engineering reasoning. Detect technical debt, calculate repository health, and generate actionable implementation blueprints.",

  keywords: [
    "RepoMind",
    "Repository Intelligence",
    "Static Analysis",
    "AST Analysis",
    "Python",
    "Developer Tools",
    "Technical Debt",
    "Engineering Intelligence",
    "AI Code Analysis",
    "Software Architecture",
    "PostgreSQL",
    "pgvector",
    "GitHub",
    "CLI",
    "Open Source",
  ],

  authors: [
    {
      name: "Noman Ahmad",
      url: "https://github.com/Noman-Ahmad25",
    },
  ],

  creator: "Noman Ahmad",

  publisher: "RepoMind",
  category: "Developer Tools",
  alternates: {
    canonical: "/",
  },

  openGraph: {
    title: "RepoMind - Repository Intelligence",
    description:
      "Evidence-driven repository intelligence powered by deterministic AST analysis and AI-assisted engineering reasoning.",
    url: "https://repomind.dev",
    siteName: "RepoMind",
    locale: "en_US",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "RepoMind - Repository Intelligence",
    description:
      "Evidence-driven repository intelligence powered by deterministic AST analysis and AI-assisted engineering reasoning.",
  },

  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-zinc-950 text-zinc-50">
        {children}
      </body>
    </html>
  );
}
