import { formatTimestamp, youtubeURL } from "@/lib/api";

type Mention = {
  episodeID: string;
  title: string;
  publishedAt: string | null;
  timestamp: number | null;
};

export default function MentionList({ mentions }: { mentions: Mention[] }) {
  if (mentions.length === 0) {
    return <p className="text-[#A1A1A1] text-sm">No episode mentions recorded.</p>;
  }

  return (
    <div className="flex flex-col">
      {mentions.map((m, i) => (
        <a
          key={i}
          href={youtubeURL(m.episodeID, m.timestamp)}
          target="_blank"
          rel="noopener noreferrer"
          className="group flex items-center gap-6 py-4 border-b border-[#E8E8E8] hover:bg-[#FFFDE0] transition-colors"
        >
          <div className="flex flex-col gap-0.5 flex-1 min-w-0">
            <span className="text-sm font-medium text-[#111111] line-clamp-1 group-hover:text-black transition-colors">
              {m.title}
            </span>
            {m.publishedAt && (
              <span className="text-xs text-[#A1A1A1]">
                {new Date(m.publishedAt).toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "short",
                  year: "numeric",
                })}
              </span>
            )}
          </div>
          {m.timestamp !== null && (
            <span
              className="text-base font-black text-[#A1A1A1] group-hover:text-[#CA9B52] transition-colors shrink-0 tabular-nums"
              style={{ fontFamily: "var(--font-barlow)" }}
            >
              {formatTimestamp(m.timestamp)}
            </span>
          )}
        </a>
      ))}
    </div>
  );
}
