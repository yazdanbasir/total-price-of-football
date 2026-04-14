import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { Playfair_Display, Barlow_Condensed, Open_Sans } from "next/font/google";
import SideNav from "@/components/SideNav";
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

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`h-full ${playfair.variable} ${barlow.variable} ${openSans.variable}`}>
      <body className="min-h-full flex flex-col bg-white text-[#464646]" style={{ fontFamily: "var(--font-open-sans)" }}>
        {/* Top header */}
        <header className="sticky top-0 z-50 bg-[#FFE200] border-b-4 border-black">
          <div className="px-6 h-14 flex items-center">
            <Link href="/" className="flex items-center">
              <Image src="/pof_logo.png" alt="Total Price of Football" height={36} width={36} style={{ height: "36px", width: "auto" }} />
            </Link>
          </div>
        </header>

        {/* Body: sidebar + content */}
        <div className="flex flex-1">
          <SideNav />

          <main className="flex-1 px-8 py-10 min-w-0">
            {children}
          </main>
        </div>

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
