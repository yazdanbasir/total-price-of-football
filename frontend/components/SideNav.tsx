import Link from "next/link";

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/glossary", label: "Glossary" },
  { href: "/directory", label: "Directory" },
  { href: "/episodes", label: "Episodes" },
];

export default function SideNav() {
  return (
    <aside className="w-52 shrink-0 border-r border-[#E8E8E8] flex flex-col px-3 pt-6 pb-6 gap-0.5">
{navLinks.map(({ href, label }) => (
        <Link
          key={href}
          href={href}
          className="px-3 py-2.5 rounded text-sm font-semibold uppercase tracking-wider text-[#464646] hover:text-black hover:bg-[#FFFDE0] border border-transparent hover:border-[#FFE200] transition-all"
        >
          {label}
        </Link>
      ))}
    </aside>
  );
}
