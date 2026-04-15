import { api } from "@/lib/api";
import GlossaryList from "@/components/GlossaryList";

export default async function GlossaryPage() {
  const data = await api.concepts.list({ limit: 1000 });

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <div className="mb-10">
        <h1
          className="text-[clamp(40px,6vw,72px)] font-black uppercase leading-[0.9] text-[#EDEBE6]"
          style={{ fontFamily: "var(--font-display)" }}
        >
          Glossary
        </h1>
        <p
          className="text-[11px] font-black uppercase tracking-[0.18em] text-[#444440] mt-4"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          {data.total} financial terms explained
        </p>
      </div>

      <GlossaryList concepts={data.concepts} />
    </div>
  );
}
