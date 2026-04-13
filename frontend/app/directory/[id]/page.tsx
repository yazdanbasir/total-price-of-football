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
    <div className="flex flex-col gap-8 max-w-2xl">
      <div className="flex flex-col gap-1">
        <Link href="/directory" className="text-xs text-[#A1A1A1] hover:text-[#CA9B52] transition-colors">
          ← Directory
        </Link>
        <div className="flex items-baseline gap-3 mt-2">
          <h1
            className="text-3xl font-normal text-[#111111]"
            style={{ fontFamily: "var(--font-playfair)" }}
          >
            {profile.name}
          </h1>
          <span className="text-xs text-[#A1A1A1] uppercase tracking-wider">{profile.type}</span>
        </div>
      </div>

      {profile.description && (
        <div className="border-l-4 border-[#FFE200] pl-4">
          <p className="text-[#464646] text-sm leading-relaxed">{profile.description}</p>
        </div>
      )}

      <div className="flex flex-col gap-3">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-[#A1A1A1]">
          Mentioned in {profile.mentions.length} episode{profile.mentions.length !== 1 ? "s" : ""}
        </h2>
        <MentionList mentions={profile.mentions} />
      </div>
    </div>
  );
}
