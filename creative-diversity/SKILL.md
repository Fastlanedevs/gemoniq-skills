---
name: creative-diversity
description: |
  Generate a diversified on-brand ad set from one source creative by changing WHY each ad works,
  not just how it looks. Takes the source creative (product anchor) plus optional brand/audience
  context, then produces variants driven by distinct customer motivators/barriers, each executed
  across differentiated formats. Default = 3 motivators x 2 formats = 6 creatives, product
  preserved, concept + format deliberately varied.
  Use when the user wants a diversified ad set, multiple hooks, ads addressing different customer
  reasons, batch creative for A/B or multi-audience testing, or "more like this" but meaningfully
  different.
  Triggers: creative diversity, diversified creatives, ad set, multi-concept ads, different hooks,
  different motivators, variants, remixes, resizes, seasonal spins, multiple backgrounds, batch
  creatives.
user-invocable: true
---

# Creative Diversity -- Motivator-Driven On-Brand Ad Sets

The user has a creative they like. This skill turns it into a diversified ad set grounded in different reasons a customer would buy, then executes each concept across differentiated formats. The product from the input creative is the **anchor** -- it stays the same in every output. Everything else (motivator, message, scene, format) deliberately changes.

Why this matters: changing *why an ad works* produces more testable, more media-mix-ready creative than changing the background or color grade of the same idea. A diversified ad set lets the delivery algorithm find the right message for the right audience; a set of cosmetic variants of the same concept just serves the same ad twice.

**The 2x2 target.** Every ad set lives on two axes: concept diversity and format diversity. The goal quadrant is the top-right -- diversified concept *and* diversified format. If two outputs share both the same motivator and the same format, they are duplicates, not diversity.

## Prerequisites

Before anything else, verify `STUDIO_API_KEY` is configured. Do this *first* -- don't gather context, identify motivators, or engineer prompts until the key is in place, otherwise the user invests effort upfront and hits a credential wall at generation time.

```bash
test -f ~/.gemoniq-studio/config.json && echo "configured" || echo "missing"
```

Also accept `STUDIO_API_KEY` exported in the environment (`echo ${STUDIO_API_KEY:+set}`).

If **missing**, ask the user inline:

> Before we generate anything, this skill needs a `STUDIO_API_KEY`. Grab one at https://app.gemoniq.com/settings/api and paste it here -- I'll save it for you.

Once the user pastes the key, save it automatically:

```bash
mkdir -p ~/.gemoniq-studio && printf '{"STUDIO_API_KEY": "%s"}\n' "<pasted-key>" > ~/.gemoniq-studio/config.json && chmod 600 ~/.gemoniq-studio/config.json
```

Don't instruct the user to run `export` or hand-edit the config -- the agent handles setup. `STUDIO_BASE_URL` is optional and defaults to `https://app.gemoniq.com`.

## Step 1: Gather Source + Context

**Required:**
- **Source creative** -- the image the user wants to diversify from. This carries the brand aesthetic (palette, typography, lighting family, mood) that every variant should inherit.

### 1a. Analyze the source creative for a product anchor

Before moving on, look at the source creative carefully and decide: does it prominently feature a specific physical product (packaging, bottle, device, garment, appliance, food item, etc.)?

**If yes -- always ask the user for additional product shots before continuing:**

> I can see a [concrete product description, e.g. "matte black skincare serum bottle with gold lettering"] in your creative. Do you have any other photos of this specific product -- different angles, a clean product shot on plain background, or other SKU variants? Adding 2-3 product images dramatically improves how consistent the product looks across the diversified set. Drop them in, or say "no" if this is the only one.

Why this matters: with a single reference, the model often hallucinates product details (wrong label text, wrong cap shape, wrong color) when the scene changes dramatically. Multiple angles anchor the product's 3D identity so it holds up under the wider scene changes that motivator diversity demands. Don't skip this ask -- it's the single biggest lever on output quality.

If no product is featured (e.g. the creative is a typographic poster, an abstract brand visual, a lifestyle scene with no hero product), skip this and treat the source creative as the sole reference.

### 1b. Other context

**Strongly recommended (each one sharpens the motivator work):**
- **Brand** -- name, category, palette, typography, tone
- **Audience** -- who the brand sells to (demographics, mindset, what they care about)
- **Constraints** -- "leave copy space top-left", "keep logo placement", "never change the bottle color", "must include the tagline"

If the user has only given you the source image and a one-liner, ask one short clarifier:

> Who's the audience for this product, and what are the main reasons they'd buy it -- or hesitate to buy it? Any constraints I should respect (leave copy space, keep logo placement, etc.)?

Don't over-interview. If the user says "just vibe it", infer the audience and motivator candidates from the creative + brand yourself and present them for approval.

## Step 2: Identify Motivators / Barriers

This is the heart of the skill. A **motivator** is a reason the customer would buy. A **barrier** is a reason they would *not* buy, which the ad addresses and removes. Both work the same way structurally; pick whichever fits each audience insight better.

Default = surface **3 distinct motivators or barriers** that are *not* already addressed in the source creative. Distinct means they come from different parts of the customer's decision -- not three rephrasings of the same need.

Propose candidates inferred from the creative + brand + audience, then let the user approve, edit, or replace. Examples of distinct motivator spans (skincare):
- *"I'm looking for dramatic, visible results"* (outcome-driven)
- *"This is exactly what my skin needs"* (fit-driven)
- *"This was recommended by a creator I trust"* (social-proof-driven)
- *"I can't pass up this deal"* (price-driven)

Examples of **non-distinct** motivators (avoid this):
- "I want soft skin" / "I want moisturized skin" / "I want hydrated skin" -- these are paraphrases, not different motivators.

Each motivator gets a **one-sentence customer-voice statement**. Writing it in the customer's own words forces specificity and keeps the downstream messaging grounded.

## Step 3: Build Benefit -> Theme for Each Motivator

For every motivator, fill in two slots:

- **Benefit** -- what is uniquely true about *this product* that answers this motivator? Not a feature list -- the single benefit that lands the motivator.
- **Theme** -- how the ad communicates that benefit. One sentence covering tone, headline direction, and visual concept.

Example, skincare, motivator = *"I'm looking for dramatic, visible results"*:
- Benefit: clinical-strength retinoid delivers visible change in 14 days.
- Theme: bold before/after energy, close-up texture, confident tone, punchy headline like "14 days. Visible difference."

## Step 4: Design the Diversity Plan

Before generating anything, draft the full plan as a single table and show it to the user. Default shape is **3 motivators x 2 formats each = 6 outputs.**

| # | Motivator | Benefit | Theme | Visual concept | Format (aspect + lo-fi/hi-fi + focus) | Prompt |
|---|-----------|---------|-------|----------------|---------------------------------------|--------|
| 1a | "dramatic visible results" | clinical retinoid, 14 days | bold before/after | macro close-up of skin texture with bottle in frame | 4:5, hi-fi, product-focused | ... |
| 1b | (same) | (same) | (same) | UGC: hand holding bottle in mirror selfie | 9:16, lo-fi, lifestyle | ... |
| 2a | "exactly what my skin needs" | precisely formulated for sensitive skin | calm, reassuring, considered | bottle on sunlit marble bathroom counter | 1:1, hi-fi, product-focused | ... |
| 2b | (same) | (same) | (same) | person in robe applying serum, morning light | 9:16, hi-fi, lifestyle | ... |
| 3a | "recommended by a creator I trust" | creator-endorsed, real users | testimonial-style, authentic | creator holding bottle, looking at camera, text overlay "worth the hype" | 9:16, lo-fi, lifestyle | ... |
| 3b | (same) | (same) | (same) | flat lay of bottle with handwritten note-style caption | 4:5, hi-fi, product-focused | ... |

**Format-within-motivator rule.** Within each motivator, the two format executions must land in *different* quadrants of the format space. Mix:
- **Aspect ratio** -- 9:16 Story/Reel, 4:5 feed, 1:1 square, 16:9 banner
- **Lo-fi vs hi-fi** -- UGC/handheld-feeling vs polished studio
- **Product-focused vs lifestyle** -- hero product shot vs human-in-context

If both of a motivator's formats are 4:5 hi-fi product shots, the row is *not* diversified -- rework it.

Show this table plus the full engineered prompts. Let the user tweak motivators, themes, formats, or prompts before generation.

## Step 5: Engineer the Prompts

Every prompt must preserve the product anchor while pushing hard on motivator and format. Prompt structure:

1. **Anchor lock (first block).** The lock language depends on which references are attached. Pick the matching case -- the explicit role labeling matters because without it the model averages across refs and product details drift.

   **Case A -- only the source creative is attached (no separate product shots):**
   > "Use the attached reference image. Keep the product design, shape, color, branding, typography, and proportions EXACTLY as shown. Only the surrounding scene, mood, framing, and composition change."

   **Case B -- source creative + product images are attached (preferred when a product is featured):**
   > "Two reference types are attached. The first image is the existing creative -- use it to match the brand palette, lighting family, typography style, and overall aesthetic direction. The remaining images are product anchor shots -- use these to keep the product's shape, color, label, branding, and proportions EXACTLY correct. If any product detail in the scene would differ from the product anchor shots, the product anchor shots win. Only the surrounding scene, mood, framing, and composition change."

2. **State the motivator-driven concept** -- what's the ad *saying*, as a felt moment. "A woman in a bathrobe lit by morning window light, calmly holding the bottle, reassured expression" lands harder than "lifestyle shot of product user".

3. **State the format delta aggressively** -- if this is the lo-fi/UGC execution, commit: handheld framing, slight imperfection, natural light, phone-camera color science. If hi-fi, commit: studio lighting, sharp product, deliberate composition. Timid deltas produce six similar-feeling ads.

4. **Respect brand DNA** -- palette, typography cues, tone from the source creative. A "diversified ad set" that abandons the brand's look isn't on-brand.

5. **Quality tail:** `masterpiece, high quality, sharp focus, 8K detail`

### Reference ordering

Always pass references in this order so the prompt's role labeling matches the actual `--ref` sequence:

1. **First ref = source creative** (the brand-aesthetic anchor)
2. **Subsequent refs = product images** (the product-identity anchors), in order of how clearly each shows the product

Cap is 4 refs per call. If the user gave more than 3 product images, pick the 3 that show the product most clearly across distinct angles (front, side, detail / label close-up). Drop redundant near-duplicates -- four shots of the same angle hurt more than they help.

For concrete language on lighting, camera/lens (lo-fi vs hi-fi control), color grading / film stocks, materiality, and text overlays, see `reference/nano-banana.md`. Consult it when you need to sharpen a prompt beyond the structural rules above -- especially when a format delta isn't landing (reach for camera/lens cues) or the mood needs to differ between motivators (reach for lighting recipes).

### Format cues to reach for

- **9:16 lo-fi / UGC** -- handheld, slight tilt, natural window light, phone color science, candid framing, hand or partial body in frame.
- **9:16 hi-fi lifestyle** -- clean vertical composition with human, editorial lighting, considered wardrobe and scene, copy space top or bottom third.
- **4:5 hi-fi product hero** -- studio or styled surface, rim light separating product, shallow depth of field, deliberate negative space.
- **4:5 lo-fi lifestyle** -- raw moment, natural imperfection, real-home feeling, documentary tone.
- **1:1 hi-fi product** -- symmetrical, iconic product pose, gallery-feeling.
- **16:9 banner** -- horizontal reflow with product weighted right-of-center, generous left negative space for headline.

## Step 6: Generate

Fire all variations in a single turn -- multiple Bash calls in parallel so the user isn't waiting serially. Each call:

```bash
python scripts/generate_image.py \
    --prompt "<engineered prompt>" \
    --output <project>/diversity/<motivator-n>_<format-label>.png \
    --aspect <ratio> \
    --size 2K \
    --ref <source_creative> \
    --ref <extra_product_image_1> \
    --ref <extra_product_image_2>
```

Name outputs so concept diversity is visible in the filename (e.g. `1a_dramatic-results_4x5-hifi-product.png`, `1b_dramatic-results_9x16-lofi-ugc.png`). The user should be able to scan a directory listing and see the motivator grouping at a glance.

**Flag reference:**
- `--prompt` -- engineered prompt (required)
- `--output` -- output file path (required)
- `--ref` -- reference image, repeatable up to 4. First ref is always the source creative.
- `--aspect` -- 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
- `--size` -- 512, 1K, 2K, 4K (default: auto)

## Step 7: Present Results

Group outputs by motivator so the user sees concept diversity first, format diversity second:

> **Motivator 1 -- "dramatic visible results":** 1a (4:5 hi-fi product), 1b (9:16 lo-fi UGC)
> **Motivator 2 -- "exactly what my skin needs":** 2a (1:1 hi-fi product), 2b (9:16 hi-fi lifestyle)
> **Motivator 3 -- "recommended by a creator":** 3a (9:16 lo-fi UGC), 3b (4:5 hi-fi product)

Offer targeted regeneration:

> If any don't land, tell me which # and what to change -- I'll regenerate just those and keep the rest.

Only regenerate flagged rows; don't redo the whole set on minor feedback.

## Project Structure

```
project_name/
  source/         # Input creative + any extra product refs
  diversity/      # Generated on-brand diversified outputs, named by motivator and format
```

## Error Recovery

- **Outputs feel like the same ad six times** -- the motivators are probably paraphrases of each other. Rewrite Step 2 so the three motivators come from genuinely different parts of the customer's decision (outcome vs fit vs social proof vs price).
- **Two outputs for the same motivator look too similar** -- the format deltas are too soft. Push harder on lo-fi vs hi-fi and lifestyle vs product-focused, not just aspect ratio.
- **Product drifts off-anchor in a scene variant** -- strengthen the lock line and pass more product reference images (up to 4). Mention specific parts the model keeps distorting: *"Keep the bottle silhouette, the label placement, and the cap color EXACTLY as in the reference."*
- **Off-brand look sneaks in** -- the prompt probably abandoned the source creative's palette and tone. Add an explicit "match the color palette, lighting family, and visual tone of the first reference image" clause.
- **API errors** -- verify `STUDIO_API_KEY` in `~/.gemoniq-studio/config.json` or env; check `STUDIO_BASE_URL` if running against a non-default server.
