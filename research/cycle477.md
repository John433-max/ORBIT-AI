# Cycle 477

Problem: several natural-language geometry asks returned no template (rectangle diagonal, rhombus area/perimeter, rectangular prism volume/surface, pyramid volume) even though coding smoke was otherwise 100%.

Implementation: `code_synth_p195.py` loaded before older packs. Matchers exclude rectangle area/perimeter, cube volume, and cone volume.

Smoke rows: code_1416–code_1421.

Fix: p194 point_distance no longer matches manhattan/chebyshev/euclidean (those stay on p173/p184). Probe after patch: all three named distances plus rectangle diagonal and pyramid volume verified.
