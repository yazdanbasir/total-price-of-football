import { api } from "@/lib/api";
import DirectoryList from "@/components/DirectoryList";

export default async function DirectoryPage() {
  const data = await api.profiles.list({ limit: 1000 });

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-1">
        <h1
          className="text-3xl font-normal text-[#111111]"
          style={{ fontFamily: "var(--font-playfair)" }}
        >
          Directory
        </h1>
        <p className="text-sm text-[#A1A1A1]">
          {data.total} clubs, people, organisations &amp; bodies discussed on the show
        </p>
      </div>

      <DirectoryList profiles={data.profiles} />
    </div>
  );
}
