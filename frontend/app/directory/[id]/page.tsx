import Link from "next/link";
import { api } from "@/lib/api";
import { notFound } from "next/navigation";
import MentionList from "@/components/MentionList";

export default async function ProfilePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let profile;
  try {
    profile = await api.profiles.get(Number(id));
  } catch {
    notFound();
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">

      <Link
        href="/directory"
        className="inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.18em] text-[#444440] hover:text-[#FFE200] transition-colors mb-10"
      >
        ← Directory
      </Link>

      <div className="flex items-baseline gap-4 mb-8">
        <h1
          className="text-[clamp(36px,5vw,64px)] font-black uppercase leading-[0.9] text-[#EDEBE6]"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          {profile.name}
        </h1>
        <span className="text-[10px] uppercase tracking-[0.15em] text-[#444440] border border-[#2A2A2A] px-2 py-1 shrink-0">
          {profile.type}
        </span>
      </div>

      {profile.description && (
        <div className="bg-[#111111] px-6 py-6 mb-12 max-w-2xl">
          <p className="text-sm text-[#BDBAB5] leading-[1.8]">
            {profile.description}
          </p>
        </div>
      )}

      <div className="flex flex-col gap-5">
        <div className="flex items-center gap-4">
          <span className="text-[11px] uppercase tracking-[0.18em] text-[#444440]">
            Mentioned in
          </span>
          <span className="text-lg font-black tabular-nums text-[#FFE200] leading-none">
            {profile.mentions.length}
          </span>
          <span className="text-[11px] uppercase tracking-[0.18em] text-[#444440]">
            episode{profile.mentions.length !== 1 ? "s" : ""}
          </span>
        </div>
        <MentionList mentions={profile.mentions} />
      </div>

    </div>
  );
}
