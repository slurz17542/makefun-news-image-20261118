// news-image-20261118 entry (Node 22, standard library only).
//
// The image this entry submits is the front page in entry.png, built at
// build time from index.html (layout) and assets/*.jpg (illustrations) and
// rendered to pixels with headless Chromium. At grading time this program
// simply places that finished image at /output/entry.png.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error(`entry image missing: ${source}`);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
