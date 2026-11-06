import type { Metadata } from "next";
import ModulePage from "@/components/ModulePage";
import { metaById, type GlossEntry } from "@/lib/modules";
import type { Question } from "@/lib/types";
import { THEORY_SE } from "@/lib/theory-se";
import questions from "@/data/usos-se.json";
import glossary from "@/data/usos-se-verbos.json";

export const metadata: Metadata = {
  title: "Los usos del se",
  description: "Os nove usos do se e a diferença entre se, sé, si e sí, do básico ao extremo.",
};

export default function Page() {
  return (
    <ModulePage
      mod={{
        ...metaById("usos-del-se"),
        questions: questions as unknown as Question[],
        theory: THEORY_SE,
        glossary: glossary as GlossEntry[],
      }}
    />
  );
}
