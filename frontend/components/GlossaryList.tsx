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
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 text-[#A1A1A1] pointer-events-none"
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          <circle cx="6.5" cy="6.5" r="5.5" stroke="currentColor" strokeWidth="1.5" />
          <path
            d="M10.5 10.5L14 14"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
        </svg>
        <input
          type="search"
          placeholder="Search terms…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full border-2 border-[#111111] pl-11 pr-10 py-4 text-base text-[#111111] placeholder:text-[#A1A1A1] focus:outline-none focus:border-[#FFE200] bg-white transition-colors"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            aria-label="Clear search"
            className="absolute right-4 top-1/2 -translate-y-1/2 text-[#A1A1A1] hover:text-[#111111] transition-colors text-xl leading-none"
          >
            ×
          </button>
        )}
      </div>

      {query && (
        <p className="text-xs text-[#A1A1A1] -mt-2">
          {filtered.length} of {concepts.length} terms
        </p>
      )}

      {filtered.length === 0 ? (
        <div className="py-16 text-center">
          <p className="text-[#A1A1A1] text-sm">No terms found for &ldquo;{query}&rdquo;.</p>
        </div>
      ) : (
        <div className="flex flex-col">
          {filtered.map((c) => (
            <Link
              key={c.id}
              href={`/glossary/${c.id}`}
              className="group flex items-center gap-6 py-5 border-b border-[#E8E8E8] -mx-8 px-8 hover:bg-[#FFFDE0] transition-colors"
            >
              <div className="flex flex-col gap-1 flex-1 min-w-0">
                <span className="text-base font-semibold text-[#111111]">
                  {c.term}
                </span>
                {c.definition && (
                  <span className="text-sm text-[#A1A1A1] line-clamp-1">
                    {c.definition}
                  </span>
                )}
              </div>
              <span className="text-sm text-[#CA9B52] opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
                →
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
