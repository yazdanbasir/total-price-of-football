"use client";

import { useState } from "react";
import Link from "next/link";
import type { Concept } from "@/lib/api";

export default function GlossaryList({ concepts }: { concepts: Concept[] }) {
  const [query, setQuery] = useState("");

  const filtered = query.trim()
    ? concepts.filter((c) =>
        c.term.toLowerCase().includes(query.toLowerCase()) ||
        c.definition?.toLowerCase().includes(query.toLowerCase())
      )
    : concepts;

  return (
    <div className="flex flex-col gap-8">
      <input
        type="search"
        placeholder="Search terms…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full max-w-md border border-[#E8E8E8] rounded px-4 py-2.5 text-sm text-[#111111] placeholder:text-[#A1A1A1] focus:outline-none focus:border-[#FFE200]"
      />

      {filtered.length === 0 ? (
        <div className="text-[#A1A1A1] text-sm">No terms found.</div>
      ) : (
        <div className="flex flex-col divide-y divide-[#E8E8E8]">
          {filtered.map((c) => (
            <Link
              key={c.id}
              href={`/glossary/${c.id}`}
              className="flex flex-col gap-1 py-4 hover:bg-[#FFFDE0] -mx-2 px-2 rounded transition-colors"
            >
              <span className="text-sm font-semibold text-[#111111]">{c.term}</span>
              {c.definition && (
                <span className="text-xs text-[#A1A1A1] line-clamp-2">{c.definition}</span>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
