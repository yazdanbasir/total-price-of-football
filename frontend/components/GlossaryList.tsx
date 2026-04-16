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
          className="absolute left-4 top-1/2 -translate-y-1/2 text-[#444440] text-xs pointer-events-none select-none"
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
        <p className="text-[12px] text-[#444440] -mt-2">
          {filtered.length} of {concepts.length} terms
        </p>
      )}

      {filtered.length === 0 ? (
        <div className="py-20 text-center">
          <p className="text-[#444440]">No terms found for &ldquo;{query}&rdquo;.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((c, i) => (
            <Link
              key={c.id}
              href={`/glossary/${c.id}`}
              className="group bg-[#151514] p-8 flex gap-8 items-center hover:bg-[#1C1C1B] transition-colors"
            >
              {/* Left marker */}
              <div
                className="shrink-0 bg-[#FFE200] flex items-center justify-center"
                style={{ width: "64px", height: "64px" }}
              >
                <span
                  className="text-[28px] font-black text-black tabular-nums leading-none"
                  style={{ fontFamily: "var(--font-barlow)" }}
                >
                  {i + 1}
                </span>
              </div>

              {/* Content */}
              <div className="flex flex-col gap-2 min-w-0 flex-1">
                <p className="text-[20px] font-semibold text-[#EDEBE6] leading-snug group-hover:text-[#FFE200] transition-colors">
                  {c.term}
                </p>
                {c.definition && (
                  <p className="text-[14px] text-[#666560] line-clamp-2 leading-relaxed">
                    {c.definition}
                  </p>
                )}
              </div>

              {/* Arrow */}
              <span className="text-[#333330] group-hover:text-[#FFE200] transition-colors text-xl shrink-0">
                →
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
