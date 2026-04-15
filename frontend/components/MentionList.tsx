import { formatTimestamp, youtubeURL } from "@/lib/api";

type Mention = {
  episodeID: string;
  title: string;
  publishedAt: string | null;
  timestamp: number | null;
};

export default function MentionList({ mentions }: { mentions: Mention[] }) {
  if (mentions.length === 0) {
    return (
      <p className="text-[#444440] py-6">No episode mentions recorded.</p>
    );
  }

  return (
    <div className="flex flex-col">
      {mentions.map((m, i) => (
        <a
          key={i}
          href={youtubeURL(m.episodeID, m.timestamp)}
          target="_blank"
          rel="noopener noreferrer"
          className="group grid grid-cols-[1fr_auto] gap-6 py-5 border-t border-[#1A1A1A] hover:bg-[#111111] transition-colors -mx-6 px-6"
        >
          <div className="flex flex-col gap-1 min-w-0">
            <span className="text-[15px] font-medium text-[#BDBAB5] line-clamp-1 group-hover:text-[#EDEBE6] transition-colors leading-snug">
              {m.title}
            </span>
            {m.publishedAt && (
              <span
                className="text-[12px] text-[#444440]"
                style={{ fontFamily: "var(--font-barlow)" }}
              >
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
              className="text-[15px] font-black text-[#333330] group-hover:text-[#FFE200] transition-colors shrink-0 tabular-nums mt-0.5"
              style={{ fontFamily: "var(--font-barlow)" }}
            >
              {formatTimestamp(m.timestamp)}
            </span>
          )}
        </a>
      ))}
      <div className="border-t border-[#1A1A1A]" />
    </div>
  );
}
