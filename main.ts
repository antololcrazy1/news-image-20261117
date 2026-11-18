// News-image entry for make.fun news-image-20261117 (Node 22, standard library only).
// The program writes one image, /output/entry.png, summing up the world news of
// Tuesday 17 November 2026: the Kerch Bridge strike, the US-Iran escalation in the
// Strait of Hormuz, Trump's Asia tour, France's nationwide strike, the Gaza aid call,
// Depardieu's admission, and the US losing measles-free status, plus a briefs strip.
// The image is the entry.png beside this file, rendered by gen_image.py (Pillow +
// DejaVu, deterministic, offline) from the day's reporting; this program copies it,
// so two runs write the same bytes. No network at run time.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Regenerate the image: python3 gen_image.py

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
