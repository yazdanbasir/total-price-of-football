import { api } from "@/lib/api";
import DirectoryList from "@/components/DirectoryList";

export default async function DirectoryPage() {
  const data = await api.profiles.list({ limit: 1000 });

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <div className="mb-10">
        <h1
          className="text-[clamp(40px,6vw,72px)] font-black uppercase leading-[0.9] text-[#EDEBE6]"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          Directory
        </h1>
        <p className="text-[12px] uppercase tracking-[0.18em] text-[#444440] mt-4">
          {data.total} clubs, people, organisations &amp; bodies
        </p>
      </div>

      <DirectoryList profiles={data.profiles} />
    </div>
  );
}
