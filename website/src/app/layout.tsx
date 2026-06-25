
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://repomind.dev"), // Replace with your domain

  title: {
    default: "RepoMind",
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

  openGraph: {
    title: "RepoMind",
    description:
      "Evidence-driven repository intelligence powered by deterministic AST analysis and AI-assisted engineering reasoning.",
    url: "https://repomind.dev", // Replace with your domain
    siteName: "RepoMind",
    locale: "en_US",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "RepoMind",
    description:
      "Evidence-driven repository intelligence powered by deterministic AST analysis and AI-assisted engineering reasoning.",
    creator: "@your_twitter", // Optional
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
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-zinc-950 text-zinc-50">
        {children}
      </body>
    </html>
  );
}

