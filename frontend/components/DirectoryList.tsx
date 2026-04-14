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
    <div className="flex flex-col gap-8">
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="search"
          placeholder="Search…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 max-w-md border border-[#E8E8E8] rounded px-4 py-2.5 text-sm text-[#111111] placeholder:text-[#A1A1A1] focus:outline-none focus:border-[#FFE200]"
        />
        <div className="flex gap-1">
          {TYPES.map((t) => (
            <button
              key={t.value}
              onClick={() => setType(t.value)}
              className={`px-3 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                type === t.value
                  ? "bg-[#FFE200] text-black"
                  : "text-[#A1A1A1] hover:text-[#464646]"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="text-[#A1A1A1] text-sm">No results found.</div>
      ) : (
        <div className="flex flex-col divide-y divide-[#E8E8E8]">
          {filtered.map((p) => (
            <Link
              key={p.id}
              href={`/directory/${p.id}`}
              className="flex items-start gap-4 py-4 hover:bg-[#FFFDE0] -mx-2 px-2 rounded transition-colors"
            >
              <span className="text-xs text-[#A1A1A1] uppercase tracking-wider pt-0.5 w-16 shrink-0">
                {p.type}
              </span>
              <div className="flex flex-col gap-0.5 min-w-0">
                <span className="text-sm font-semibold text-[#111111]">{p.name}</span>
                {p.description && (
                  <span className="text-xs text-[#A1A1A1] line-clamp-2">{p.description}</span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
