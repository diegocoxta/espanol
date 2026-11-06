import type { ComponentType, ReactNode } from "react";
import { MODULES } from "@/lib/modules";

type LinkLike = ComponentType<{ href: string; className?: string; children: ReactNode; "aria-current"?: "page" }>;

/** Abas entre os cadernos. Na app Next usa next/link; no artefato, âncoras com #hash. */
export default function ModuleNav({
  current,
  LinkComp,
  hrefFor,
}: {
  current: string;
  LinkComp?: LinkLike;
  hrefFor?: (id: string, href: string) => string;
}) {
  const A: LinkLike = LinkComp ?? (({ href, className, children, ...rest }) => (
    <a href={href} className={className} {...rest}>
      {children}
    </a>
  ));
  return (
    <nav className="modnav" aria-label="Cadernos">
      {MODULES.map((m) => (
        <A
          key={m.id}
          href={hrefFor ? hrefFor(m.id, m.href) : m.href}
          className={`modtab${m.id === current ? " on" : ""}`}
          aria-current={m.id === current ? "page" : undefined}
        >
          <b>{m.tab}</b>
          <span>{m.tabSub}</span>
        </A>
      ))}
    </nav>
  );
}
