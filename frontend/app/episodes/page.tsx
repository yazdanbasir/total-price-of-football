import { api } from "@/lib/api";

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
  const data = await api.episodes.list({ limit: 100 });

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-1">
        <h1
          className="text-3xl font-normal text-[#111111]"
          style={{ fontFamily: "var(--font-playfair)" }}
        >
          Episodes
        </h1>
        <p className="text-sm text-[#A1A1A1]">{data.total} episodes</p>
      </div>

      <div className="flex flex-col">
        {data.episodes.map((ep) => (
          <a
            key={ep.youtubeID}
            href={`https://www.youtube.com/watch?v=${ep.youtubeID}`}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-5 py-5 border-b border-[#E8E8E8] -mx-8 px-8 hover:bg-[#FFFDE0] transition-colors"
          >
            {ep.thumbnail && (
              <img
                src={ep.thumbnail}
                alt=""
                className="w-28 h-[63px] object-cover shrink-0"
              />
            )}
            <div className="flex flex-col gap-1.5 flex-1 min-w-0">
              <span className="text-sm font-semibold text-[#111111] line-clamp-2 leading-snug group-hover:text-black transition-colors">
                {ep.title}
              </span>
              <div className="flex items-center gap-2 text-xs text-[#A1A1A1]">
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
            <span className="text-sm text-[#CA9B52] opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
              →
            </span>
          </a>
        ))}
      </div>
    </div>
  );
}
