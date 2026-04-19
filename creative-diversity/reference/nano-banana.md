# Nano Banana -- Minimal Reference for Ad Diversity

Quick cheat sheet for engineering prompts in `creative-diversity`. Use this when you need concrete language for lighting, camera, grading, or text overlay. For the full framework see `ai-creative-studio/reference/nano-banana.md`.

## Prompt shape (for every variant)

```
[Anchor lock]  Use attached references. Keep product shape/color/branding/typography EXACTLY.
[Concept]      What the ad is saying, as a felt moment (motivator-driven).
[Scene]        Environment with materiality -- specific surfaces, light, mood.
[Camera]       Lens + film stock + framing.
[Grade]        Color grading / palette language.
[Quality tail] masterpiece, high quality, sharp focus, 8K detail.
```

Write in **full sentences**, not keyword soup. Nano Banana reasons about the prompt; it rewards direction over tags.

## Lighting

Pick one per ad. Lighting carries more mood than any other single choice.

| Mood | Prompt language |
|------|-----------------|
| Studio product / polished | Three-point softbox setup, rim light separating subject from background |
| Dramatic / bold | Chiaroscuro, single hard key from above-left, deep shadows |
| Warm / romantic | Golden hour backlighting, long soft shadows, warm fill |
| Calm / clean | Soft diffused north-facing window light, no harsh shadows |
| UGC / authentic | Natural daylight through a window, slight overexposure, no fill |
| Atmospheric | Tyndall beams through dusty air, volumetric god rays |

## Camera & lens (lo-fi vs hi-fi control)

This is how you hit the format-within-motivator rule. Pick hardware that matches the format quadrant.

**Hi-fi / polished:**
- `Hasselblad medium-format, 85mm, f/2.8, shallow depth of field` -- editorial product hero
- `Fujifilm 35mm, f/4, natural color science` -- considered lifestyle
- `medium-format analog film, fine grain, rich tonality` -- premium brand feel

**Lo-fi / UGC / authentic:**
- `iPhone front-camera selfie, handheld, slight motion` -- mirror UGC
- `phone-camera color science, slight overexposure, candid framing` -- native social feel
- `cheap disposable camera flash aesthetic, raw, grainy` -- nostalgic UGC
- `GoPro wide angle, immersive, slight barrel distortion` -- action/POV

**Framing language:** close-up, macro, medium shot, full shot, low angle, eye-level, bird's-eye, POV. Generous negative space for headline copy; rule-of-thirds when placing product off-center.

## Color grading / film stocks

Cite specific stocks instead of adjectives. "Kodak Portra 400" beats "warm tones".

| Feel | Language |
|------|----------|
| Warm editorial | Kodak Portra 400 color science, amber and cream tones |
| Cool desaturated | Fuji Pro 400H, muted teal, soft pastel palette |
| Cinematic blockbuster | Teal-and-orange color grade, high contrast |
| Punchy social | Vibrant saturation, Instagram-native grade |
| Nostalgic / gritty | 1980s color film, slight grain, faded blacks |
| Premium minimal | Low saturation, high key, clean whites |

Always inherit the source creative's palette direction unless the motivator deliberately pushes a seasonal or campaign-specific shift.

## Materiality (specific wins)

Generic descriptions produce generic images. Be concrete about the non-product surfaces around the anchor product:

| Generic | Specific |
|---------|----------|
| counter | sunlit Carrara marble countertop with soft vein detail |
| table | reclaimed oak tabletop with visible grain and wax finish |
| fabric | crumpled ivory linen with natural slubs |
| background | warm terracotta plaster wall with subtle texture |
| light | morning light filtered through sheer linen curtains |

## Text overlays (for ads with headlines)

1. **Use quotes:** `"14 days. Visible difference."`
2. **Name the font family:** `bold condensed sans-serif`, `elegant serif`, `handwritten script`
3. **Specify placement:** `top third`, `lower-left corner`, `centered over negative space`
4. **Call out the material if stylized:** `3D block letters with soft drop shadow`, `embossed foil`
5. **Text-first trick:** if the text keeps coming out broken, ask the model to write the line first as text, then run a second pass to render it in the image.

Keep headlines short (2-5 words). Long copy rarely renders cleanly; pair short headline + implied supporting copy space.

## Reference images -- two roles, label them in the prompt

References do double duty: one says "this is the brand look", others say "this is the exact product." The model averages across refs unless you tell it which is which, so always disambiguate the roles in the prompt text.

**Ordering (always):**
1. First `--ref` = source creative (brand aesthetic anchor: palette, lighting, typography, mood)
2. Subsequent `--ref`s = product images (product identity anchors: shape, label, color, branding)

Cap is 4 refs total. If you have more than 3 product shots, keep the 3 most distinct angles (front + side + detail/label close-up); drop near-duplicates.

**Lock language by case:**

- *Source creative only:* "Use the attached reference image. Keep the product design, shape, color, branding, typography, and proportions EXACTLY as shown."
- *Source creative + product images:* "Two reference types are attached. The first image is the existing creative -- use it to match the brand palette, lighting family, typography style, and aesthetic direction. The remaining images are product anchor shots -- use these to keep the product's shape, color, label, branding, and proportions EXACTLY correct. If any product detail in the scene would differ from the product anchor shots, the product anchor shots win."

**When the product is still distorting:** name the specific part that keeps breaking. *"Keep the bottle silhouette, label placement, and cap color EXACTLY as in the product reference shots."* Generic locks slip; named-part locks hold.

## Quality tail

Append to every prompt: `masterpiece, high quality, sharp focus, 8K detail`. One line, always at the end.

## Golden rules

1. Full sentences, not keywords.
2. Positive framing -- "empty street" beats "no cars".
3. One strong verb up front -- *render*, *photograph*, *capture*.
4. Specific materials beat generic nouns.
5. Control the camera explicitly (lens + film stock + angle).
6. Keep the anchor lock line first, always.
