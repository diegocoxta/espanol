import raw from "@/data/questions.json";
import type { Question } from "./types";

/** Caderno 1 — objeto direto e indireto */
export const QUESTIONS = raw as unknown as Question[];
