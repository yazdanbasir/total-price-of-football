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

      <div className="flex flex-col divide-y divide-[#E8E8E8]">
        {data.episodes.map((ep) => (
          <a
            key={ep.youtubeID}
            href={`https://www.youtube.com/watch?v=${ep.youtubeID}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-start gap-4 py-4 hover:bg-[#FFFDE0] -mx-2 px-2 rounded transition-colors group"
          >
            {ep.thumbnail && (
              <img
                src={ep.thumbnail}
                alt=""
                className="w-24 h-14 object-cover rounded shrink-0"
              />
            )}
            <div className="flex flex-col gap-1 min-w-0">
              <span className="text-sm font-semibold text-[#111111] line-clamp-2 leading-snug">
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
                    <span>·</span>
                    <span>{parseDuration(ep.duration)}</span>
                  </>
                )}
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
