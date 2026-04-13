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
    <div className="flex flex-col gap-2">
      {mentions.map((m, i) => (
        <a
          key={i}
          href={youtubeURL(m.episodeID, m.timestamp)}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-between gap-4 p-3 border border-[#E8E8E8] rounded hover:border-[#FFE200] hover:bg-[#FFFDE0] transition-all group"
        >
          <div className="flex flex-col gap-0.5 min-w-0">
            <span className="text-sm text-[#111111] font-medium truncate">{m.title}</span>
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
            <span className="text-xs text-[#A1A1A1] font-mono shrink-0 group-hover:text-[#CA9B52] transition-colors">
              {formatTimestamp(m.timestamp)}
            </span>
          )}
        </a>
      ))}
    </div>
  );
}
