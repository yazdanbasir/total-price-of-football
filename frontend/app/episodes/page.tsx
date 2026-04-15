import { api, youtubeURL } from "@/lib/api";

function parseDuration(iso: string | null): string {
  if (!iso) return "";
  const match = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!match) return "";
  const h = parseInt(match[1] || "0");
  const m = parseInt(match[2] || "0");
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

export default async function EpisodesPage() {
  const { total } = await api.episodes.list({ limit: 1 });
  const data = await api.episodes.list({ limit: total });

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">

      <div className="mb-12">
        <h1
          className="text-[clamp(40px,6vw,72px)] font-black uppercase leading-[0.9] text-[#EDEBE6]"
          style={{ fontFamily: "var(--font-display)" }}
        >
          Episodes
        </h1>
        <p
          className="text-[12px] font-black uppercase tracking-[0.18em] text-[#444440] mt-4"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          {data.total} episodes archived
        </p>
      </div>

      <div className="flex flex-col">
        {data.episodes.map((ep, i) => (
          <a
            key={ep.youtubeID}
            href={youtubeURL(ep.youtubeID)}
            target="_blank"
            rel="noopener noreferrer"
            className="group grid grid-cols-[56px_1fr] gap-6 py-5 border-t border-[#1E1E1E] hover:bg-[#141414] transition-colors -mx-6 px-6"
          >
            <span
              className="text-[12px] font-black tabular-nums text-[#2E2E2C] group-hover:text-[#FFE200] transition-colors pt-0.5"
              style={{ fontFamily: "var(--font-barlow)" }}
            >
              {String(data.total - i).padStart(3, "0")}
            </span>
            <div className="flex flex-col gap-1.5">
              <span className="text-[15px] font-medium text-[#BDBAB5] line-clamp-2 leading-snug group-hover:text-[#EDEBE6] transition-colors">
                {ep.title}
              </span>
              <div
                className="flex items-center gap-3 text-[12px] text-[#444440]"
                style={{ fontFamily: "var(--font-barlow)" }}
              >
                {ep.publishedAt && (
                  <span>
                    {new Date(ep.publishedAt).toLocaleDateString("en-GB", {
                      day: "numeric",
                      month: "short",
                      year: "numeric",
                    })}
                  </span>
                )}
                {ep.duration && (
                  <>
                    <span aria-hidden="true">·</span>
                    <span>{parseDuration(ep.duration)}</span>
                  </>
                )}
              </div>
            </div>
          </a>
        ))}
        <div className="border-t border-[#1E1E1E]" />
      </div>

    </div>
  );
}
