import type { Metadata } from "next";
import ModulePage from "@/components/ModulePage";
import { metaById, type GlossEntry } from "@/lib/modules";
import type { Question } from "@/lib/types";
import { THEORY_PRON } from "@/lib/theory-pronominales";
import questions from "@/data/pronominales.json";
import glossary from "@/data/pronominales-verbos.json";

export const metadata: Metadata = {
  title: "Verbos con pronombre",
  description: "Tipo gustar, pronominais, reflexivos, recíprocos e ênfase: todos os verbos da lista, do básico ao extremo.",
};

export default function Page() {
  return (
    <ModulePage
      mod={{
        ...metaById("pronominales"),
        questions: questions as unknown as Question[],
        theory: THEORY_PRON,
        glossary: glossary as GlossEntry[],
      }}
    />
  );
}
