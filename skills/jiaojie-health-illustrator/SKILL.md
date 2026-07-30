---
name: jiaojie-health-illustrator
description: Use when a user asks for WeChat illustrations, warm hand-drawn health infographics, an illustrated publishing package, or an optional upload to the WeChat Official Account draft box for Chinese health-science or wellness content supplied as DOCX, Markdown, HTML, plain text, or pasted text.
---

# Jiaojie Health Illustrator

Create consistent raster illustrations and a verified local WeChat publishing package for Chinese health-science articles.

## Important Claude Code limitation

Claude Code does not provide Codex's native `imagegen`. A Claude Code installation can complete raster illustrations only when the user has separately configured an image-capable backend such as `baoyu-image-gen` or an image MCP tool. Without one, stop after the health review, illustration outline, and saved prompts; do not claim that PNGs, illustrated HTML, or the final ZIP were produced. Draft-box upload also requires the separate `baoyu-post-to-wechat` Skill, Bun, Chrome, and a logged-in WeChat Official Account session. Read [references/agent-compatibility.md](references/agent-compatibility.md) before promising a complete Claude Code run.

## Scope and exclusions

Use this Skill for exercise, rehabilitation and function, nutrition, weight management and body composition, women's midlife and menopause health, sleep and circadian health, mental wellbeing and emotion regulation, and other lifestyle or preventive-health education.

Do not use it for generic non-health articles, layout-only work, single posters, or video frames. Do not diagnose, prescribe individualized treatment, change medication, or provide crisis intervention. Generate local files by default. Upload to the WeChat draft box only when the user explicitly asks for it; never mass-publish or send to followers.

Defaults are 3–5 illustrations, 3:2 landscape, warm cream paper, black hand-drawn linework, soft macaron color blocks, and concise Chinese labels. Explicit instructions in the current request override style, palette, ratio, count, and delivery scope.

## Required companion skills

- Use `docx` to read `.docx` inputs. Preserve the original and extract or convert into a derivative Markdown file.
- Use `baoyu-article-illustrator` to analyze positions, confirm settings, save prompts before generation, and resolve a raster backend.
- In Codex, use the native `imagegen` raster backend unless the user explicitly chooses another available backend. In Claude Code, use an installed raster backend such as `baoyu-image-gen` or an image MCP tool.
- Use `baoyu-post-to-wechat` for local WeChat-compatible HTML and, only after an explicit user request, optional draft-box upload. Never invoke mass-publish or follower-send actions.
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

### 9. Run the self-growth loop

Read [references/self-growth.md](references/self-growth.md) after each task unless the user says “本次不记录成长数据”. Generate a package-local `growth/retrospective.md` that records evidence-based observations about health wording, illustrations, layout, validation, and draft saving. Extract preference candidates separately from confirmed preferences; apply only confirmed preferences on later tasks.

Keep growth records local. Never record article text, credentials, cookies, tokens, or unnecessary personal health information. Do not upload growth records automatically.

Treat public Skill changes as a separate C-class action. If a candidate improvement might be promoted to the public Skill, first show the exact proposed rule, evidence, affected files, and version/release plan. Modify the public Skill, commit to GitHub, or create a release only after the user explicitly replies “确认”. Without that confirmation, keep the proposal local and marked `待确认`.

### 10. Optionally upload to the WeChat draft box

Run this stage only when the user explicitly asks to upload, send, save, or publish the article to the WeChat Official Account draft box. Read [references/wechat-draft.md](references/wechat-draft.md). Obtain one action-time confirmation after the final package is validated, then pass the derivative Markdown—not the pre-converted HTML—to `baoyu-post-to-wechat`.

Resolve author or editor identity in this order: current user instruction, article frontmatter, selected account configuration, then empty. Never hardcode the Skill creator's name, `Jiaojie`, or any other identity into a public installation.

Treat draft saving and mass publishing as different actions. Stop after the draft is saved. Report whether saving was fully automatic, completed after user interaction, or unverified. Never infer automatic success merely because an `appmsgid` appears after the user manually clicked Save.

## Failure and degradation rules

- In every pre-generation plan, name the selected or expected raster backend and state the no-backend degradation path, even when the current runtime appears to have a backend.
- If no raster backend is available, stop after analysis, risk notes, outline, and saved prompts. Explicitly state that PNGs, final HTML, and ZIP were not produced.
- If one image fails, retry that image once and preserve successful images.
- If Chinese labels are wrong, create a corrected versioned prompt and regenerate; never patch the bitmap.
- If a consequential health claim cannot be verified, use conservative wording and mark it for professional review rather than inventing support.
- If HTML conversion fails, preserve Markdown and images but do not call the result a complete publishing package.
- If draft upload fails, preserve the validated local package and state that only the optional draft stage failed.
- If automatic draft saving is not independently confirmed, leave the populated editor open for manual saving and report the result as unverified until the user confirms it.
- If a dependency is missing, name it precisely and request authorization before installing a locked dependency.

## Reference routing

- Read [references/health-safety.md](references/health-safety.md) for topic boundaries, claim checks, and disclaimer tiers.
- Read [references/visual-system.md](references/visual-system.md) before planning or reviewing images.
- Read [references/prompt-recipes.md](references/prompt-recipes.md) before writing prompts.
- Read [references/output-contract.md](references/output-contract.md) before creating delivery files or validating a package.
- Read [references/agent-compatibility.md](references/agent-compatibility.md) when selecting a backend or running outside Codex.
- Read [references/wechat-draft.md](references/wechat-draft.md) before any login, upload, or draft-save action.
- Read [references/self-growth.md](references/self-growth.md) after each task for the A+B self-growth loop and the C-class public-update confirmation gate.
- Read [references/usage-examples.md](references/usage-examples.md) when the requested trigger or override behavior is ambiguous.
