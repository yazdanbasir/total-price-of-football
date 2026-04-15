"use client";

import { useState } from "react";
import Link from "next/link";
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
            className="absolute left-4 top-1/2 -translate-y-1/2 text-[#444440] text-xs font-black pointer-events-none select-none"
            style={{ fontFamily: "var(--font-barlow)" }}
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

        <div className="flex items-center gap-1">
          {TYPES.map((t) => (
            <button
              key={t.value}
              onClick={() => setType(t.value)}
              className={`px-3 py-1.5 text-[11px] font-black uppercase tracking-[0.15em] transition-colors ${
                type === t.value
                  ? "bg-[#FFE200] text-black"
                  : "bg-[#111111] text-[#555550] hover:text-[#EDEBE6] hover:bg-[#1A1A1A]"
              }`}
              style={{ fontFamily: "var(--font-barlow)" }}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {(query || type) && (
        <p
          className="text-[12px] text-[#444440] -mt-2"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          {filtered.length} of {profiles.length} entries
        </p>
      )}

      {filtered.length === 0 ? (
        <div className="py-20 text-center">
          <p className="text-[#444440]">No results found.</p>
        </div>
      ) : (
        <div className="flex flex-col">
          {filtered.map((p) => (
            <Link
              key={p.id}
              href={`/directory/${p.id}`}
              className="group grid grid-cols-[1fr_auto] gap-6 py-6 border-t border-[#1A1A1A] -mx-6 px-6 hover:bg-[#111111] transition-colors"
            >
              <div className="flex flex-col gap-1.5 min-w-0">
                <div className="flex items-center gap-3">
                  <span className="text-[17px] font-semibold text-[#BDBAB5] group-hover:text-[#EDEBE6] transition-colors leading-snug">
                    {p.name}
                  </span>
                  <span
                    className="text-[9px] font-black uppercase tracking-[0.15em] text-[#333330] border border-[#222220] px-1.5 py-0.5 shrink-0"
                    style={{ fontFamily: "var(--font-barlow)" }}
                  >
                    {p.type}
                  </span>
                </div>
                {p.description && (
                  <p className="text-[15px] text-[#555550] line-clamp-1 leading-relaxed">
                    {p.description}
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
