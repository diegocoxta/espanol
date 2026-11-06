import ModulePage from "@/components/ModulePage";
import { metaById } from "@/lib/modules";
import { QUESTIONS } from "@/lib/questions";
import { THEORY } from "@/lib/theory";

export default function Page() {
  return <ModulePage mod={{ ...metaById("objeto"), questions: QUESTIONS, theory: THEORY }} />;
}
