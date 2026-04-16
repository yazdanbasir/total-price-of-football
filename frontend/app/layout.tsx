import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { Bricolage_Grotesque, Big_Shoulders } from "next/font/google";
import HeaderNavLink from "@/components/HeaderNavLink";
import "./globals.css";

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
});

const bigShoulders = Big_Shoulders({
  subsets: ["latin"],
  weight: ["700", "800", "900"],
  variable: "--font-barlow",
});

export const metadata: Metadata = {
  title: "Total Price of Football",
  description: "Every financial term, club, and story from the Price of Football podcast.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`h-full ${bricolage.className} ${bigShoulders.variable}`}>
      <body className="min-h-full flex flex-col bg-[#0A0A0A] text-[#EDEBE6]">
        <header className="sticky top-0 z-50 bg-[#FFE200] border-b-4 border-black">
          <div className="px-6 h-14 flex items-center relative">

            {/* Left: logo */}
            <Link href="/" className="flex items-center shrink-0">
              <Image
                src="/pof_logo.png"
                alt="Total Price of Football"
                height={48}
                width={48}
                style={{ height: "48px", width: "auto" }}
              />
            </Link>

            {/* Center: site name */}
            <div className="absolute left-1/2 -translate-x-1/2 pointer-events-none select-none">
              <span
                className="font-black uppercase whitespace-nowrap"
                style={{ fontFamily: "var(--font-barlow)", color: "#000000", fontSize: "27px", letterSpacing: "0.04em", fontWeight: 900 }}
              >
                Total Price of Football
              </span>
            </div>

            {/* Right: nav */}
            <nav className="ml-auto flex items-center gap-1" aria-label="Site navigation">
              <HeaderNavLink href="/glossary">Glossary</HeaderNavLink>
              <HeaderNavLink href="/directory">Directory</HeaderNavLink>
              <HeaderNavLink href="/episodes">Episodes</HeaderNavLink>
            </nav>

          </div>
        </header>

        <main className="flex-1">
          {children}
        </main>

        <footer className="border-t border-[#1E1E1E] text-[#666560] text-[14px] text-center py-6">
          A fan project. All content from{" "}
          <a
            href="https://www.youtube.com/@POF_POD"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-[#CA9B52] underline transition-colors"
          >
            The Price of Football
          </a>{" "}
          by Kevin Day &amp; Kieran Maguire.
        </footer>
      </body>
    </html>
  );
}
