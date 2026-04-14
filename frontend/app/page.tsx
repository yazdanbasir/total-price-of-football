import Link from "next/link";
import { api } from "@/lib/api";

export default async function Home() {
  const [concepts, profiles, episodes] = await Promise.all([
    api.concepts.list({ limit: 1 }),
    api.profiles.list({ limit: 1 }),
    api.episodes.list({ limit: 1 }),
  ]);

  return (
    <div className="flex flex-col gap-12 py-12">
      {/* Hero */}
      <div className="flex flex-col gap-5">
        <p className="text-xs font-bold uppercase tracking-widest text-[#CA9B52]">
          The Price of Football — Complete Archive
        </p>
        <h1
          className="text-6xl font-normal leading-[1.05] text-[#111111]"
          style={{ fontFamily: "var(--font-playfair)" }}
        >
          Football finance, <em>fully documented.</em>
        </h1>
        <p className="text-base leading-relaxed text-[#464646]">
          {episodes.total} episodes. Every financial term, club, person, and
          story — timestamped and linked to the exact moment it was covered on
          the{" "}
          <a
            href="https://www.youtube.com/@POF_POD"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#CA9B52] hover:underline"
          >
            Price of Football
          </a>{" "}
          podcast.
        </p>
      </div>

      {/* Section index */}
      <div className="flex flex-col">
        <div className="border-t-2 border-[#111111]" />

        <Link
          href="/glossary"
          className="group flex items-center gap-8 py-7 border-b border-[#E8E8E8] -mx-8 px-8 hover:bg-[#FFFDE0] transition-colors"
        >
          <span
            className="text-5xl font-black text-[#111111] w-20 shrink-0 tabular-nums"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {concepts.total}
          </span>
          <div className="flex flex-col gap-1 flex-1 min-w-0">
            <span className="text-lg font-semibold text-[#111111]">Glossary</span>
            <span className="text-sm text-[#A1A1A1]">
              Financial terms &amp; regulations explained
            </span>
          </div>
          <span className="text-sm text-[#CA9B52] opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all shrink-0">
            Browse →
          </span>
        </Link>

        <Link
          href="/directory"
          className="group flex items-center gap-8 py-7 border-b border-[#E8E8E8] -mx-8 px-8 hover:bg-[#FFFDE0] transition-colors"
        >
          <span
            className="text-5xl font-black text-[#111111] w-20 shrink-0 tabular-nums"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {profiles.total}
          </span>
          <div className="flex flex-col gap-1 flex-1 min-w-0">
            <span className="text-lg font-semibold text-[#111111]">Directory</span>
            <span className="text-sm text-[#A1A1A1]">
              Clubs, people, organisations &amp; bodies
            </span>
          </div>
          <span className="text-sm text-[#CA9B52] opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all shrink-0">
            Browse →
          </span>
        </Link>

        <Link
          href="/episodes"
          className="group flex items-center gap-8 py-7 border-b border-[#E8E8E8] -mx-8 px-8 hover:bg-[#FFFDE0] transition-colors"
        >
          <span
            className="text-5xl font-black text-[#111111] w-20 shrink-0 tabular-nums"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {episodes.total}
          </span>
          <div className="flex flex-col gap-1 flex-1 min-w-0">
            <span className="text-lg font-semibold text-[#111111]">Episodes</span>
            <span className="text-sm text-[#A1A1A1]">
              Browse the full podcast archive
            </span>
          </div>
          <span className="text-sm text-[#CA9B52] opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all shrink-0">
            Browse →
          </span>
        </Link>
      </div>
    </div>
  );
}
