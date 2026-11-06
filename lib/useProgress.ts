"use client";

import { useCallback, useEffect, useState } from "react";
import type { Store } from "./types";

const DEFAULT_STORE: Store = { r: {}, lv: 1, mode: "seq", type: "all", pos: {}, verb: null };

function read(key: string): Store {
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return DEFAULT_STORE;
    const parsed = JSON.parse(raw);
    return { ...DEFAULT_STORE, ...parsed, r: parsed.r ?? {}, pos: parsed.pos ?? {}, verb: parsed.verb ?? null };
  } catch {
    return DEFAULT_STORE;
  }
}

/**
 * Progresso e preferências de um caderno, persistidos no localStorage sob `storageKey`.
 * `ready` só fica true depois de ler o navegador — antes disso a página
 * renderiza um estado neutro, evitando divergência de hidratação.
 */
export function useProgress(storageKey: string) {
  const [store, setStore] = useState<Store>(DEFAULT_STORE);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setStore(read(storageKey));
    setReady(true);
    const onStorage = (e: StorageEvent) => {
      if (e.key === storageKey) setStore(read(storageKey));
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, [storageKey]);

  useEffect(() => {
    if (!ready) return;
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(store));
    } catch {
      /* modo privado ou armazenamento bloqueado: segue sem salvar */
    }
  }, [store, ready, storageKey]);

  const update = useCallback((fn: (s: Store) => Store) => setStore(fn), []);
  const resetProgress = useCallback(() => setStore((s) => ({ ...s, r: {}, pos: {} })), []);

  return { store, update, ready, resetProgress };
}
