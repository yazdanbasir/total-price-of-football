import type { Metadata } from "next";
import Link from "next/link";
import { Playfair_Display, Barlow_Condensed, Open_Sans } from "next/font/google";
import "./globals.css";

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
});

const barlow = Barlow_Condensed({
  subsets: ["latin"],
  weight: ["700", "800", "900"],
  variable: "--font-barlow",
});

const openSans = Open_Sans({
  subsets: ["latin"],
  variable: "--font-open-sans",
});

export const metadata: Metadata = {
  title: "Total Price of Football",
  description: "Every financial term, club, and story from the Price of Football podcast.",
};

function Nav() {
  return (
    <header className="sticky top-0 z-50 bg-black border-b-4 border-[#FFE200]">
      <div className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
        <Link
          href="/"
          className="font-black uppercase tracking-tight text-[#FFE200] text-lg leading-none"
          style={{ fontFamily: "var(--font-barlow)" }}
        >
          Total Price of Football
        </Link>
        <nav
          className="flex items-center gap-6 text-xs font-semibold uppercase tracking-widest text-white/70"
          style={{ fontFamily: "var(--font-open-sans)" }}
        >
          <Link href="/glossary" className="hover:text-[#FFE200] transition-colors">Glossary</Link>
          <Link href="/directory" className="hover:text-[#FFE200] transition-colors">Directory</Link>
          <Link href="/episodes" className="hover:text-[#FFE200] transition-colors">Episodes</Link>
        </nav>
      </div>
    </header>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`h-full ${playfair.variable} ${barlow.variable} ${openSans.variable}`}>
      <body className="min-h-full flex flex-col bg-white text-[#464646]" style={{ fontFamily: "var(--font-open-sans)" }}>
        <Nav />
        <main className="flex-1 max-w-5xl mx-auto w-full px-6 py-10">
          {children}
        </main>
        <footer className="border-t border-[#E8E8E8] text-[#A1A1A1] text-xs text-center py-6">
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
