# Swarm Pepe — pixel art scene

## Result

| Field | Value |
|---|---|
| Output | `artifacts/image.png` |
| Format | PNG, 8-bit RGBA, non-interlaced |
| Dimensions | 1024 × 1024 px (square) |
| Logical grid | 128 × 128 pixel-art cells, each rendered as an 8 × 8 block |
| Renderer | provided `render_svg_to_png` tool (resvg), from hand-authored SVG |
| Agents in scene | 263 tiny 4×4-cell robot sprites (gold head, black visor, green body) |

Scene: a large pixel-art Pepe head (green skin, heavy eyelids, gold-brown lips)
centred on a near-black background, surrounded by a dense swarm of tiny AI agents.
The lower-right part of Pepe is still "under construction": it is drawn as a dark
scaffold grid with a dotted dark-gold blueprint outline and freshly placed gold
blocks, with agents carrying gold blocks clustered around it and dotted gold data
trails converging on it. A row of agents stands on top of the head. A gold pixel
border frames the composition, with a 2×-scale 3×5 pixel-font title "SWARM PEPE"
at the top and a caption "263 AGENTS BUILDING" at the bottom.

Palette: greens (#3f8f2e, #2a6a20, #5fb445, #1d3a16), golds (#f0c232, #c9a227,
#a67f14), lip browns (#b57a2b, #7a4c17), eye white, black, background #070a06.

## How it was made

`src/generate_scene.py` builds the 128×128 cell grid procedurally (head from
unioned ellipses, eyes, lips, scaffold region, pixel font, rejection-sampled agent
placement with a fixed random seed) and emits a compact SVG where each colour is
one path of 1-cell-high horizontal strokes. `src/scene.svg` is the exact markup that
was rendered. Re-running the script reproduces the same SVG.

## Visual requirements check

| Requirement | Status |
|---|---|
| Pixel art / retro 8-bit style | Met (hard 8×8 blocks, no anti-aliasing, limited palette) |
| Swarm Pepe as the subject | Met (recognisable Pepe head; stylised, procedurally drawn) |
| Hundreds of tiny AI agents | Met (263 sprites) |
| Agents building the image together | Met (unbuilt scaffold region, carried blocks, data trails, agents on the head) |
| Green and gold colours | Met |
| Dark background | Met |
| Square composition | Met (1024 × 1024) |

## Limitations

- The image is vector-authored pixel art, not a diffusion render. Pepe is a
  simplified procedural likeness rather than a traced reference drawing.
- "Hundreds" is satisfied with 263 agents; the agent count is limited by the
  128-cell grid and the 4×4 sprite size with spacing.
- The renderer rejects `<use>`/`<defs>`, so sprites are stamped into the grid and
  emitted as paths. This has no visual effect.
- Visual quality was checked by eye on a local resvg render that is pixel-identical
  to the delivered file; no independent human review step was run.
