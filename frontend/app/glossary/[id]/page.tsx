import Link from "next/link";
import { api } from "@/lib/api";
import { notFound } from "next/navigation";
import MentionList from "@/components/MentionList";

export default async function ConceptPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let concept;
  try {
    concept = await api.concepts.get(Number(id));
  } catch {
    notFound();
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">

      <Link
        href="/glossary"
        className="inline-flex items-center gap-2 text-[11px] font-black uppercase tracking-[0.18em] text-[#444440] hover:text-[#FFE200] transition-colors mb-10"
        style={{ fontFamily: "var(--font-barlow)" }}
      >
        ← Glossary
      </Link>

      <h1
        className="text-[clamp(36px,5vw,64px)] font-black uppercase leading-[0.9] text-[#EDEBE6] mb-8"
        style={{ fontFamily: "var(--font-display)" }}
      >
        {concept.term}
      </h1>

      {concept.definition && (
        <div className="bg-[#111111] px-6 py-6 mb-12 max-w-2xl">
          <p className="text-sm text-[#BDBAB5] leading-[1.8]">
            {concept.definition}
          </p>
        </div>
      )}

      <div className="flex flex-col gap-5">
        <div className="flex items-center gap-4">
          <span
            className="text-[11px] font-black uppercase tracking-[0.18em] text-[#444440]"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            Mentioned in
          </span>
          <span
            className="text-lg font-black tabular-nums text-[#FFE200] leading-none"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            {concept.mentions.length}
          </span>
          <span
            className="text-[11px] font-black uppercase tracking-[0.18em] text-[#444440]"
            style={{ fontFamily: "var(--font-barlow)" }}
          >
            episode{concept.mentions.length !== 1 ? "s" : ""}
          </span>
        </div>
        <MentionList mentions={concept.mentions} />
      </div>

    </div>
  );
}
