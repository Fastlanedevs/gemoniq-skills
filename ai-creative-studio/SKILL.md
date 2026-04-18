---
name: ai-creative-studio
description: |
  AI Creative Studio -- on-brand image production pipeline.
  Takes brand details, product images, reference images, and creative direction,
  then engineers a highly technical Nano Banana prompt and generates the image.
  Use when: generating product shots, brand imagery, marketing visuals, mood boards, concept art, or any image
  from loose creative direction.
  Trigger words: image, generate image, product shot, brand image, visual, render, photo, creative, studio, on-brand.
user-invocable: true
---

# AI Creative Studio -- On-Brand Image Production

Takes loose creative context and converts it into a highly technical Nano Banana 2 prompt, then generates the image.

## Prerequisites

**Before doing anything else, verify the `STUDIO_API_KEY` is configured.** Do this check *first* — do not gather context, engineer prompts, or run any generation commands until the key is in place. Otherwise the user invests effort upfront and only hits a credential prompt at the end of the workflow.

Run this check:

```bash
test -f ~/.gemoniq-studio/config.json && echo "configured" || echo "missing"
```

Also accept `STUDIO_API_KEY` exported in the environment (`echo ${STUDIO_API_KEY:+set}`).

If **missing**, ask the user inline:

> Before we generate anything, this skill needs a `STUDIO_API_KEY`. Grab one at https://app.gemoniq.com/settings/api and paste it here — I'll save it to `~/.gemoniq-studio/config.json` for you so you don't have to set it up again.

Once the user pastes the key, save it for them automatically:

```bash
mkdir -p ~/.gemoniq-studio && printf '{"STUDIO_API_KEY": "%s"}\n' "<pasted-key>" > ~/.gemoniq-studio/config.json && chmod 600 ~/.gemoniq-studio/config.json
```

Do **not** instruct the user to run `export` or hand-edit the config file themselves — the agent handles setup. `STUDIO_BASE_URL` is optional and defaults to `https://app.gemoniq.com`.

## Step 1: Gather Context

Collect the following from the user (all optional except specific context):

| Input | Description | Used For |
|-------|-------------|----------|
| **Brand details** | Name, visual identity, colors, typography, tone | Style, color grading, mood |
| **Product images** | ALL available photos/renders of the product (multiple angles, variants) | `--ref` flags for consistency -- pass ALL, not just one |
| **Reference image** | Mood board, inspiration, style reference | `--ref` flag for style/tone |
| **Specific context** | What the image should depict, purpose, audience, platform | Subject, scenario, composition |

If the user provides everything upfront, skip to Step 2. Otherwise ask concise clarifying questions.

## Step 2: Engineer the Prompt

Transform user context into a technical Nano Banana prompt using the Creative Director framework (see `reference/nano-banana.md`).

Build the prompt with these components in order:

1. **Subject** -- specific description of what's in frame (product, person, scene). Use precise materiality: "matte ceramic jar with gold foil label" not "a jar".
2. **Action/Scenario** -- what's happening, the narrative moment.
3. **Environment** -- where, with atmospheric details (surfaces, background elements, depth).
4. **Lighting** -- choose a technique that matches brand tone:
   - Premium/luxury → "Three-point softbox setup, rim light separating subject from background"
   - Bold/dramatic → "Chiaroscuro lighting, single hard light source from above-left"
   - Warm/approachable → "Golden hour backlighting, soft fill, long shadows"
   - Clean/minimal → "Soft diffused north-facing window light, no harsh shadows"
5. **Camera/Lens** -- match to purpose:
   - Product hero shot → "Medium-format analog film, 85mm, f/2.8, shallow depth of field"
   - Lifestyle/context → "Fujifilm, 35mm, f/4, natural color science"
   - Social media → "iPhone-style, candid framing, slight overexposure"
   - Editorial → "Hasselblad, center-framed, generous negative space"
6. **Color grading** -- derived from brand palette:
   - Specify exact tones: "warm amber and cream tones" not "warm colors"
   - Reference film stocks if appropriate: "Kodak Portra 400 color science"
7. **Style** -- overall aesthetic (e.g., "editorial photography", "3D product render", "fashion magazine").
8. **Quality tags** -- append: "masterpiece, high quality, sharp focus, 8K detail"

**When reference images are provided:**
- Prepend: "Use the attached reference images."
- If product ref: "Keep the product design, shape, color, and branding exactly as shown in the reference."
- If style ref: "Match the mood, color palette, and visual tone of the reference image."

**CRITICAL -- Multi-Reference Rule:**
When the user provides multiple images of the same product (different angles, colors, contexts), you MUST pass ALL of them as `--ref` flags (up to 4). More references = better product consistency. A single reference often causes the model to hallucinate product details. Always prefer passing 2-4 product images over just 1.

**Show the engineered prompt to the user before generating.** Let them tweak if needed.

## Step 3: Generate

Run the generation script:

```bash
python scripts/generate_image.py \
    --prompt "<engineered prompt>" \
    --output <output_path>.png \
    --aspect <ratio> \
    --size 2K \
    --ref <product_image_1> \
    --ref <product_image_2> \
    --ref <product_image_3> \
    --ref <style_reference>
```

**Credentials.** Already handled in the Prerequisites step above. The script also reads the same `~/.gemoniq-studio/config.json` or `STUDIO_API_KEY` env var as a fallback.

**Flag reference:**
- `--prompt` -- the engineered prompt (required)
- `--output` -- output file path (required)
- `--ref` -- reference image, repeatable up to 4. **ALWAYS pass all available product images** (optional)
- `--edit` -- source image for editing/inpainting (optional)
- `--aspect` -- aspect ratio, default 16:9 (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)
- `--size` -- resolution: 512, 1K, 2K, 4K (default: none/auto)

**Default aspect ratios by purpose:**
- Product hero → 1:1 or 4:5
- Social post → 1:1 or 4:5
- Website banner → 16:9 or 21:9
- Story/reel → 9:16
- Print ad → 3:4 or 2:3

## Project Structure

```
project_name/
  refs/           # Input reference images (product photos, mood boards)
  output/         # Generated images
```

## Error Recovery

- **Prompt too vague** → add materiality, lighting technique, camera details
- **Product not matching ref** → strengthen lock: "Keep product EXACTLY as shown. Same shape, same label, same colors."
- **Wrong mood/tone** → adjust lighting and color grading descriptors
- **Text rendering issues** → use Nano Banana Pro model: `--model gemini-3-pro-image-preview`
- **API errors** → verify `STUDIO_API_KEY` in `~/.gemoniq-studio/config.json` or env; check `STUDIO_BASE_URL` if running against a non-default server
