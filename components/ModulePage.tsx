"use client";

import Link from "next/link";
import StudyApp from "./StudyApp";
import ModuleNav from "./ModuleNav";
import type { ModuleDef } from "@/lib/modules";

/** Página de um caderno na app Next (navegação entre cadernos com next/link). */
export default function ModulePage({ mod }: { mod: ModuleDef }) {
  return <StudyApp mod={mod} nav={<ModuleNav current={mod.id} LinkComp={Link} />} />;
}
