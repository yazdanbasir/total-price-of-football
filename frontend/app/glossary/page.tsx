"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { api, type Concept } from "@/lib/api";

export default function GlossaryPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q: initialQ } = use(searchParams);
  const [query, setQuery] = useState(initialQ || "");
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const timeout = setTimeout(() => {
      api.concepts
        .list({ search: query, limit: 500 })
        .then((data) => {
          setConcepts(data.concepts);
          setTotal(data.total);
        })
        .finally(() => setLoading(false));
    }, 200);
    return () => clearTimeout(timeout);
  }, [query]);

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-1">
        <h1
          className="text-3xl font-normal text-[#111111]"
          style={{ fontFamily: "var(--font-playfair)" }}
        >
          Glossary
        </h1>
        <p className="text-sm text-[#A1A1A1]">
          {total} financial terms &amp; regulations explained on the show
        </p>
      </div>

      <input
        type="search"
        placeholder="Search terms…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full max-w-md border border-[#E8E8E8] rounded px-4 py-2.5 text-sm text-[#111111] placeholder:text-[#A1A1A1] focus:outline-none focus:border-[#FFE200]"
      />

      {loading ? (
        <div className="text-[#A1A1A1] text-sm">Loading…</div>
      ) : concepts.length === 0 ? (
        <div className="text-[#A1A1A1] text-sm">No terms found.</div>
      ) : (
        <div className="flex flex-col divide-y divide-[#E8E8E8]">
          {concepts.map((c) => (
            <Link
              key={c.id}
              href={`/glossary/${c.id}`}
              className="flex flex-col gap-1 py-4 hover:bg-[#FFFDE0] -mx-2 px-2 rounded transition-colors"
            >
              <span className="text-sm font-semibold text-[#111111]">{c.term}</span>
              {c.definition && (
                <span className="text-xs text-[#A1A1A1] line-clamp-2">
                  {c.definition}
                </span>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
