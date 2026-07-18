---
name: jiaojie-health-illustrator
description: Use when a user asks for WeChat illustrations, warm hand-drawn health infographics, or an illustrated publishing package for Chinese health-science or wellness content supplied as DOCX, Markdown, HTML, plain text, or pasted text.
---

# Jiaojie Health Illustrator

Create consistent raster illustrations and a verified local WeChat publishing package for Chinese health-science articles.

## Scope and exclusions

Use this Skill for exercise, rehabilitation and function, nutrition, weight management and body composition, women's midlife and menopause health, sleep and circadian health, mental wellbeing and emotion regulation, and other lifestyle or preventive-health education.

Do not use it for generic non-health articles, layout-only work, single posters, or video frames. Do not diagnose, prescribe individualized treatment, change medication, or provide crisis intervention. Generate local files only; never log in to, submit to, or mass-publish through WeChat unless the user separately asks for publishing.

Defaults are 3–5 illustrations, 3:2 landscape, warm cream paper, black hand-drawn linework, soft macaron color blocks, and concise Chinese labels. Explicit instructions in the current request override style, palette, ratio, count, and delivery scope.

## Required companion skills

- Use `docx` to read `.docx` inputs. Preserve the original and extract or convert into a derivative Markdown file.
- Use `baoyu-article-illustrator` to analyze positions, confirm settings, save prompts before generation, and resolve a raster backend.
- In Codex, use the native `imagegen` raster backend unless the user explicitly chooses another available backend. In Claude Code, use an installed raster backend such as `baoyu-image-gen` or an image MCP tool.
- Use `baoyu-post-to-wechat` for the local WeChat-compatible HTML workflow. Do not invoke its submit or publishing actions.
- Browse authoritative sources when a health claim is unstable, consequential, high-risk, or cannot be checked reliably from the supplied article.

## Workflow

### 1. Preserve and read the source

Record the source path and SHA-256 before work. Never edit the supplied source in place. For pasted content, save a source copy inside a newly named working directory. Create the publishing package in a separate `公众号发布包/<文章主题>/` directory.

### 2. Scan health claims and choose the disclaimer tier

Read [references/health-safety.md](references/health-safety.md). Flag guarantees, universal timelines, causal certainty, unsourced percentages, and instructions presented as suitable for everyone. Verify consequential claims with authoritative sources when required. Show proposed wording changes separately from the unchanged source.

Choose the disclaimer tier from the article's actual risk. Do not paste one long disclaimer mechanically into every article. Tier 3 content requires safety routing, not merely a disclaimer.

### 3. Plan 3–5 useful illustrations

Read [references/visual-system.md](references/visual-system.md). Use the article's structure rather than a fixed four-image template. Select only positions where a visual improves understanding: cover, mechanism or process, contrast, framework, or action list. For every item state its position, purpose, visual content, exact short labels, type, and filename in `imgs/outline.md`.

### 4. Ask for one confirmation

Present one compact confirmation covering illustration count and positions, visual system, ratio, palette, language, and health wording changes. Do not render images until the user confirms.

Skip this gate only when the current request explicitly says “直接生成”, “不用确认”, “跳过确认”, “按默认出图”, or equivalent. Before rendering, state the assumptions being applied.

### 5. Save prompts before generation

Read [references/prompt-recipes.md](references/prompt-recipes.md). Save one complete prompt per image to `imgs/prompts/NN-{type}-{slug}.md` before invoking any raster backend. Include exact Chinese labels, composition, palette, aspect ratio, health-accuracy constraints, and negative constraints. Never pass an unsaved ad-hoc prompt directly to the backend.

### 6. Generate and inspect raster images

Resolve the backend using [references/agent-compatibility.md](references/agent-compatibility.md) and the companion illustrator's backend-selection rules. Generate from saved prompts, then move or copy final PNGs into `imgs/` without overwriting earlier candidates.

Inspect every image for Chinese accuracy, clinical meaning, consistent visual language, requested ratio, safe margins, and watermarks. Retry only failed images once with a new versioned prompt and filename. Never repair generated text by painting over the bitmap with Python, ImageMagick, Canvas, SVG, HTML, or CSS.

### 7. Assemble Markdown, WeChat HTML, and ZIP

Read [references/output-contract.md](references/output-contract.md). Insert relative PNG references into a derivative `*_文章源稿.md`. Use `baoyu-post-to-wechat` to produce local WeChat-compatible HTML while explicitly stopping before login or submission. Create the sibling publishing ZIP only after Markdown, HTML, prompts, and PNGs are final.

Recompute the source SHA-256 and confirm it matches the pre-work value.

### 8. Validate before claiming completion

Run `scripts/validate_package.py` with the actual count and ratio overrides. A run is complete only when the validator prints `PACKAGE_OK`, the ZIP exists, and the original hash is unchanged. Report absolute paths and list any publishing action that was intentionally not performed.

## Failure and degradation rules

- If no raster backend is available, stop after analysis, risk notes, outline, and saved prompts. Explicitly state that PNGs, final HTML, and ZIP were not produced.
- If one image fails, retry that image once and preserve successful images.
- If Chinese labels are wrong, create a corrected versioned prompt and regenerate; never patch the bitmap.
- If a consequential health claim cannot be verified, use conservative wording and mark it for professional review rather than inventing support.
- If HTML conversion fails, preserve Markdown and images but do not call the result a complete publishing package.
- If a dependency is missing, name it precisely and request authorization before installing a locked dependency.

## Reference routing

- Read [references/health-safety.md](references/health-safety.md) for topic boundaries, claim checks, and disclaimer tiers.
- Read [references/visual-system.md](references/visual-system.md) before planning or reviewing images.
- Read [references/prompt-recipes.md](references/prompt-recipes.md) before writing prompts.
- Read [references/output-contract.md](references/output-contract.md) before creating delivery files or validating a package.
- Read [references/agent-compatibility.md](references/agent-compatibility.md) when selecting a backend or running outside Codex.
- Read [references/usage-examples.md](references/usage-examples.md) when the requested trigger or override behavior is ambiguous.
