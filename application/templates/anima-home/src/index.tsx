import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BruceAboutUs } from "./screens/BruceAboutUs";

createRoot(document.getElementById("app") as HTMLElement).render(
  <StrictMode>
    <BruceAboutUs />
  </StrictMode>,
);
