export const dynamic = "force-dynamic";

import Link from "next/link";
import Image from "next/image";
import { api } from "@/lib/api";
import { siYoutube, siSpotify, siApplepodcasts } from "simple-icons";

export default async function Home() {
  const [concepts, profiles, episodes] = await Promise.all([
    api.concepts.list({ limit: 1 }),
    api.profiles.list({ limit: 1 }),
    api.episodes.list({ limit: 1 }),
  ]);

  const stats = [
    { href: "/glossary", count: concepts.total, label: "Terms" },
    { href: "/directory", count: profiles.total, label: "Profiles" },
  ];

  return (
    <div>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-14 pb-10 text-center">
        <p className="text-[17px] text-[#888580] max-w-xl mx-auto leading-relaxed mb-8">
          The Price of Football - Complete Archive
        </p>

        <h1
          className="uppercase font-black leading-[0.88] text-[#EDEBE6] mb-3"
          style={{
            fontFamily: "var(--font-barlow)",
            fontSize: "clamp(52px, 9vw, 108px)",
          }}
        >
          Football Finance,
        </h1>
        <h1
          className="uppercase font-black leading-[0.88] text-[#FFE200] mb-12"
          style={{
            fontFamily: "var(--font-barlow)",
            fontSize: "clamp(52px, 9vw, 108px)",
          }}
        >
          Fully Documented.
        </h1>

        <p className="text-[17px] text-[#888580] mx-auto leading-relaxed whitespace-nowrap">
          Every financial term, club, person, and story as covered on the <a href="https://www.youtube.com/@POF_POD" target="_blank" rel="noopener noreferrer" className="text-[#CA9B52] hover:text-[#FFE200] transition-colors">Price of Football</a> podcast :)
        </p>
      </section>

      {/* Stats bar */}
      <div>
        <div className="max-w-3xl mx-auto grid grid-cols-2 border border-[#1E1E1E]">
          {stats.map((s, i) => (
            <Link
              key={s.href}
              href={s.href}
              className={`group flex flex-col gap-2 py-8 px-6 h-full hover:bg-[#141414] transition-colors ${i < stats.length - 1 ? "border-r border-[#1E1E1E]" : ""}`}
            >
              <span
                className="text-[clamp(36px,5vw,56px)] font-black leading-none tabular-nums text-[#EDEBE6] group-hover:text-[#FFE200] transition-colors"
                style={{ fontFamily: "var(--font-barlow)" }}
              >
                {s.count}
              </span>
              <span className="text-[14px] font-semibold uppercase tracking-[0.18em] text-[#666560] group-hover:text-[#888580] transition-colors">
                {s.label} →
              </span>
            </Link>
          ))}
        </div>
      </div>

      {/* Latest episode */}
      {episodes.episodes[0] && (() => {
        const ep = episodes.episodes[0];
        const listenLinks = [
          {
            label: "YouTube",
            href: "https://www.youtube.com/@POF_POD",
            icon: siYoutube,
          },
          {
            label: "Spotify",
            href: "https://open.spotify.com/show/7c7ltYVwnicbVz0uYTXAW5",
            icon: siSpotify,
          },
          {
            label: "Apple",
            href: "https://podcasts.apple.com/gb/podcast/the-price-of-football/id1482886394",
            icon: siApplepodcasts,
          },
          {
            label: "Website",
            href: "https://priceoffootball.com",
            icon: null,
          },
        ];

        return (
          <section className="max-w-6xl mx-auto px-6 py-12">
            <div className="flex items-center justify-between mb-8">
              <span className="text-[14px] uppercase tracking-[0.2em] text-[#666560]">
                Latest Episode
              </span>
            </div>

            <div className="bg-[#151514] p-8 flex gap-8 items-center">

              {/* Logo */}
              <Image
                src="/logo.png"
                alt="Price of Football"
                width={80}
                height={80}
                className="shrink-0"
                style={{ width: "80px", height: "80px", objectFit: "contain" }}
              />

              {/* Content */}
              <div className="flex flex-col gap-5 min-w-0 flex-1">
                <div className="flex flex-col gap-2">
                  {ep.publishedAt && (
                    <span className="text-[14px] uppercase tracking-[0.18em] text-[#666560]">
                      {new Date(ep.publishedAt).toLocaleDateString("en-GB", {
                        day: "numeric",
                        month: "long",
                        year: "numeric",
                      })}
                    </span>
                  )}
                  <p className="text-[20px] font-semibold text-[#EDEBE6] leading-snug">
                    {ep.title}
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  {listenLinks.map((link) => (
                    <a
                      key={link.label}
                      href={link.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-4 py-2 bg-[#282826] hover:bg-[#FFE200] text-[#888580] hover:text-black transition-colors"
                    >
                      {link.icon ? (
                        <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4 shrink-0" aria-hidden="true">
                          <path d={link.icon.path} />
                        </svg>
                      ) : (
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4 shrink-0" aria-hidden="true">
                          <circle cx="12" cy="12" r="10"/>
                          <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                        </svg>
                      )}
                      <span className="text-[13px] font-semibold uppercase tracking-[0.12em]">
                        {link.label}
                      </span>
                    </a>
                  ))}
                </div>
              </div>

            </div>
          </section>
        );
      })()}

    </div>
  );
}
