"use client";

import { useState } from "react";
import type { Profile } from "@/lib/api";

const TYPES = [
  { value: "", label: "All" },
  { value: "person", label: "People" },
  { value: "club", label: "Clubs" },
  { value: "organisation", label: "Orgs" },
  { value: "body", label: "Bodies" },
];


export default function DirectoryList({ profiles }: { profiles: Profile[] }) {
  const [query, setQuery] = useState("");
  const [type, setType] = useState("");

  const filtered = profiles.filter((p) => {
    const matchesType = !type || p.type === type;
    const matchesQuery =
      !query.trim() ||
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.description?.toLowerCase().includes(query.toLowerCase());
    return matchesType && matchesQuery;
  });

  return (
    <div className="flex flex-col gap-6">
      {/* Search + filter */}
      <div className="flex flex-col gap-3">
        <div className="relative">
          <span
            className="absolute left-4 top-1/2 -translate-y-1/2 text-[#444440] text-xs pointer-events-none select-none"
            aria-hidden="true"
          >
            /
          </span>
          <input
            type="search"
            placeholder="Search…"
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

        <div className="flex items-center gap-1">
          {TYPES.map((t) => (
            <button
              key={t.value}
              onClick={() => setType(t.value)}
              className={`px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.15em] transition-colors ${
                type === t.value
                  ? "bg-[#FFE200] text-black"
                  : "bg-[#111111] text-[#555550] hover:text-[#EDEBE6] hover:bg-[#1A1A1A]"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {(query || type) && (
        <p className="text-[12px] text-[#444440] -mt-2">
          {filtered.length} of {profiles.length} entries
        </p>
      )}

      {filtered.length === 0 ? (
        <div className="py-20 text-center">
          <p className="text-[#444440]">No results found.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((p, i) => (
            <div
              key={p.id}
              className="bg-[#151514] p-8 flex gap-8 items-center hover:bg-[#1C1C1B] transition-colors"
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
                <div className="flex items-center gap-3">
                  <p className="text-[20px] font-semibold text-[#EDEBE6] leading-snug">
                    {p.name}
                  </p>
                  <span className="text-[10px] uppercase tracking-[0.15em] text-[#444440] border border-[#2A2A2A] px-1.5 py-0.5 shrink-0">
                    {p.type}
                  </span>
                </div>
                {p.description && (
                  <p className="text-[14px] text-[#666560] line-clamp-2 leading-relaxed">
                    {p.description}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
