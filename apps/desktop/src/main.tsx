import React from "react";
import { createRoot } from "react-dom/client";
import { providerIds } from "@open-course-compiler/shared";

function App() {
  return <main><h1>Open Course Compiler</h1><p>Stage 1 foundation ready for {providerIds.join(" and ")}.</p></main>;
}

createRoot(document.getElementById("root")!).render(<App />);
