import { loader } from "@monaco-editor/react";

export function configureMonaco() {
  if (typeof window === "undefined") {
    return;
  }

  // Use local dev resources to avoid initial bundle initialization anomalies.
  loader.config({
    paths: {
      vs: "/monaco-editor/dev/vs",
    },
  });
}
