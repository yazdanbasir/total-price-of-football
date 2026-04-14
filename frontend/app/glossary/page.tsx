import { api } from "@/lib/api";
import GlossaryList from "@/components/GlossaryList";

export default async function GlossaryPage() {
  const data = await api.concepts.list({ limit: 1000 });

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
          {data.total} financial terms &amp; regulations explained on the show
        </p>
      </div>

      <GlossaryList concepts={data.concepts} />
    </div>
  );
}
