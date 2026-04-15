"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function HeaderNavLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isActive = pathname.startsWith(href);

  return (
    <Link
      href={href}
      className={`px-3 py-1.5 text-[20px] font-black uppercase tracking-[0.12em] transition-colors ${
        isActive ? "bg-black" : "hover:bg-black/10"
      }`}
      style={{
        fontFamily: "var(--font-barlow)",
        color: isActive ? "#FFE200" : "#000000",
      }}
    >
      {children}
    </Link>
  );
}
