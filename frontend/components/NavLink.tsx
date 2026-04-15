"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function NavLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isActive = href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <Link
      href={href}
      className={`px-5 py-3.5 text-[11px] font-black uppercase tracking-[0.18em] transition-colors ${
        isActive
          ? "text-[#FFE200]"
          : "text-[#555550] hover:text-[#EDEBE6]"
      }`}
      style={{ fontFamily: "var(--font-barlow)" }}
    >
      {children}
    </Link>
  );
}
