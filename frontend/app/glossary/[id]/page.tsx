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
    <div className="flex flex-col gap-8 max-w-2xl">
      <div className="flex flex-col gap-1">
        <Link href="/glossary" className="text-xs text-[#A1A1A1] hover:text-[#CA9B52] transition-colors">
          ← Glossary
        </Link>
        <h1
          className="text-3xl font-normal text-[#111111] mt-2"
          style={{ fontFamily: "var(--font-playfair)" }}
        >
          {concept.term}
        </h1>
      </div>

      {concept.definition && (
        <div className="border-l-4 border-[#FFE200] pl-4">
          <p className="text-[#464646] text-sm leading-relaxed">{concept.definition}</p>
        </div>
      )}

      <div className="flex flex-col gap-3">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-[#A1A1A1]">
          Mentioned in {concept.mentions.length} episode{concept.mentions.length !== 1 ? "s" : ""}
        </h2>
        <MentionList mentions={concept.mentions} />
      </div>
    </div>
  );
}
