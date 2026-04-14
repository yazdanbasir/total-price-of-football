"use client";

import { useState } from "react";
import Link from "next/link";
import type { Profile } from "@/lib/api";

const TYPES = [
  { value: "", label: "All" },
  { value: "person", label: "People" },
  { value: "club", label: "Clubs" },
  { value: "organisation", label: "Organisations" },
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
            placeholder="Search…"
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

        <div className="flex gap-2 flex-wrap">
          {TYPES.map((t) => (
            <button
              key={t.value}
              onClick={() => setType(t.value)}
              className={`px-4 py-1.5 text-xs font-semibold uppercase tracking-wider transition-colors ${
                type === t.value
                  ? "bg-[#FFE200] text-black"
                  : "bg-[#F5F5F5] text-[#464646] hover:bg-[#FFFDE0] hover:text-black"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {(query || type) && (
        <p className="text-xs text-[#A1A1A1] -mt-2">
          {filtered.length} of {profiles.length} entries
        </p>
      )}

      {filtered.length === 0 ? (
        <div className="py-16 text-center">
          <p className="text-[#A1A1A1] text-sm">No results found.</p>
        </div>
      ) : (
        <div className="flex flex-col">
          {filtered.map((p) => (
            <Link
              key={p.id}
              href={`/directory/${p.id}`}
              className="group flex items-center gap-6 py-5 border-b border-[#E8E8E8] -mx-8 px-8 hover:bg-[#FFFDE0] transition-colors"
            >
              <div className="flex flex-col gap-1 flex-1 min-w-0">
                <div className="flex items-baseline gap-3 min-w-0">
                  <span className="text-base font-semibold text-[#111111]">
                    {p.name}
                  </span>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-[#A1A1A1] shrink-0">
                    {p.type}
                  </span>
                </div>
                {p.description && (
                  <span className="text-sm text-[#A1A1A1] line-clamp-1">
                    {p.description}
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
