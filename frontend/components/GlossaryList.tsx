"use client";

import { useState } from "react";
import Link from "next/link";
import type { Concept } from "@/lib/api";

export default function GlossaryList({ concepts }: { concepts: Concept[] }) {
  const [query, setQuery] = useState("");

  const filtered = query.trim()
    ? concepts.filter(
        (c) =>
          c.term.toLowerCase().includes(query.toLowerCase()) ||
          c.definition?.toLowerCase().includes(query.toLowerCase())
      )
    : concepts;

  return (
    <div className="flex flex-col gap-6">
      {/* Search */}
      <div className="relative">
        <span
          className="absolute left-4 top-1/2 -translate-y-1/2 text-[#444440] text-xs font-black pointer-events-none select-none"
          style={{ fontFamily: "var(--font-barlow)" }}
          aria-hidden="true"
        >
          /
        </span>
        <input
          type="search"
          placeholder="Search terms…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full bg-[#111111] border border-[#2A2A2A] focus:border-[#FFE200] pl-8 pr-10 py-4 text-base text-[#EDEBE6] placeholder:text-[#333330] focus:outline-none transition-colors"
          style={{ fontFamily: "var(--font-barlow)" }}
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            aria-label="Clear search"
            className="absolute right-4 top-1/2 -translate-y-1/2 text-[#444440] hover:text-[#EDEBE6] transition-colors text-lg leading-none"
          >
            ×
          </button>
        )}
      </div>

      {query && (
        <p
          className="text-[12px] text-[#444440] -mt-2"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          {filtered.length} of {concepts.length} terms
        </p>
      )}

      {filtered.length === 0 ? (
        <div className="py-20 text-center">
          <p className="text-[#444440]">No terms found for &ldquo;{query}&rdquo;.</p>
        </div>
      ) : (
        <div className="flex flex-col">
          {filtered.map((c) => (
            <Link
              key={c.id}
              href={`/glossary/${c.id}`}
              className="group grid grid-cols-[1fr_auto] gap-6 py-6 border-t border-[#1A1A1A] -mx-6 px-6 hover:bg-[#111111] transition-colors"
            >
              <div className="flex flex-col gap-2 min-w-0">
                <span className="text-[17px] font-semibold text-[#BDBAB5] group-hover:text-[#EDEBE6] transition-colors leading-snug">
                  {c.term}
                </span>
                {c.definition && (
                  <p className="text-[15px] text-[#555550] line-clamp-2 leading-relaxed">
                    {c.definition}
                  </p>
                )}
              </div>
              <span
                className="text-xs font-black text-[#2A2A28] group-hover:text-[#FFE200] transition-colors mt-1 shrink-0"
                style={{ fontFamily: "var(--font-barlow)" }}
              >
                →
              </span>
            </Link>
          ))}
          <div className="border-t border-[#1A1A1A]" />
        </div>
      )}
    </div>
  );
}
