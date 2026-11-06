"use client";

import { useState } from "react";

export default function ResetButton({ onConfirm }: { onConfirm: () => void }) {
  const [asking, setAsking] = useState(false);

  if (!asking)
    return (
      <button className="linkbtn" onClick={() => setAsking(true)}>
        Apagar progresso
      </button>
    );

  return (
    <span className="confirm">
      Apagar todas as respostas?
      <button
        className="linkbtn danger"
        onClick={() => {
          onConfirm();
          setAsking(false);
        }}
      >
        Apagar
      </button>
      <button className="linkbtn" onClick={() => setAsking(false)}>
        Cancelar
      </button>
    </span>
  );
}
