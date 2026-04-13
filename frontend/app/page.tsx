import Link from "next/link";
import { api } from "@/lib/api";

export default async function Home() {
  const [concepts, profiles, episodes] = await Promise.all([
    api.concepts.list({ limit: 1 }),
    api.profiles.list({ limit: 1 }),
    api.episodes.list({ limit: 1 }),
  ]);

  return (
    <div className="flex flex-col gap-16 py-12">
      <div className="flex flex-col gap-4 max-w-2xl">
        <h1
          className="text-5xl font-normal leading-tight text-[#111111]"
          style={{ fontFamily: "var(--font-playfair)" }}
        >
          The full archive of football finance,{" "}
          <span className="text-[#A1A1A1]">explained.</span>
        </h1>
        <p className="text-base leading-relaxed text-[#464646]">
          Every financial term, club, person, and story discussed on the{" "}
          <a
            href="https://www.youtube.com/@POF_POD"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#CA9B52] hover:underline"
          >
            Price of Football
          </a>{" "}
          podcast — timestamped, searchable, and linked back to the exact
          moment it was covered.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Link
          href="/glossary"
          className="flex flex-col gap-2 p-6 border border-[#E8E8E8] rounded hover:border-[#FFE200] hover:bg-[#FFFDE0] transition-all group"
        >
          <span
            className="text-4xl font-black text-[#111111] group-hover:text-black"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {concepts.total}
          </span>
          <span className="text-sm font-semibold uppercase tracking-wider text-[#111111]">Glossary</span>
          <span className="text-xs text-[#A1A1A1]">
            Financial terms &amp; regulations explained
          </span>
        </Link>
        <Link
          href="/directory"
          className="flex flex-col gap-2 p-6 border border-[#E8E8E8] rounded hover:border-[#FFE200] hover:bg-[#FFFDE0] transition-all group"
        >
          <span
            className="text-4xl font-black text-[#111111]"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {profiles.total}
          </span>
          <span className="text-sm font-semibold uppercase tracking-wider text-[#111111]">Directory</span>
          <span className="text-xs text-[#A1A1A1]">
            Clubs, people, organisations &amp; bodies
          </span>
        </Link>
        <Link
          href="/episodes"
          className="flex flex-col gap-2 p-6 border border-[#E8E8E8] rounded hover:border-[#FFE200] hover:bg-[#FFFDE0] transition-all group"
        >
          <span
            className="text-4xl font-black text-[#111111]"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {episodes.total}
          </span>
          <span className="text-sm font-semibold uppercase tracking-wider text-[#111111]">Episodes</span>
          <span className="text-xs text-[#A1A1A1]">
            Browse the full podcast archive
          </span>
        </Link>
      </div>
    </div>
  );
}
