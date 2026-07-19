# 提示词配方

## 文件规则

每张图先保存一个完整提示词文件：`imgs/prompts/NN-{type}-{slug}.md`。提示词确认存在后才能调用位图后端。文件与 PNG 使用相同编号和 slug。

## 主模板

```text
Use case: scientific-educational
Asset type: Chinese WeChat article illustration
Article topic: {文章主题}
Image role: {cover | process | comparison | framework | action-list}
Primary message: {这一张图必须讲清的唯一结论}
Position in article: {标题或段落之后}

Scene and subjects:
{人物、物体、身体部位或抽象元素；只写文章真正需要的内容}

Information structure:
{画面分区、阅读顺序、箭头和层级；最多 3–5 个核心节点}

Chinese text, render verbatim:
- "{主标题}"
- "{标签一}"
- "{标签二}"
{继续列出必要标签；不要增加未列出的文字}

Style:
Warm cream paper background #F7F0E4, charcoal-black hand-drawn linework #262421,
soft macaron color blocks using coral #E98B7B, mint #A9CDB8, sky #A9C6DE,
butter yellow #E9CC78, and muted purple #B9ADD2. Friendly editorial health infographic,
light pencil texture, clean flat shapes, generous whitespace, calm and credible.

Composition:
3:2 landscape, mobile-readable labels, at least 8% safe margins, one dominant idea,
clear visual hierarchy, balanced negative space.

Health accuracy constraints:
{不能夸大的关系、必须保留的条件、不能画成标准动作处方的内容}

Avoid:
photorealism, glossy 3D, dense paragraphs, tiny text, garbled Chinese, extra labels,
invented medical devices, diagnostic certainty, body shaming, fear-based imagery,
logos, signatures, watermarks, QR codes, borders, and decorative English text.
```

## 图型追加段

### Cover

```text
Use one memorable visual metaphor grounded in the article's real concept. Keep the title dominant and leave calm breathing room. Do not literalize a metaphor in a medically misleading way.
```

### Process

```text
Arrange 3–5 steps in one direction. Use consistent arrows and show conditions beside the relevant step. Do not imply that every reader follows the same recovery timeline.
```

### Comparison

```text
Use equal-size panels and compare the same dimension on both sides. Separate "常见误区" from "更稳妥做法" without shaming the reader.
```

### Framework

```text
Place the central concept in the middle and limit branches to 3–5. Give each branch one icon and one short label; keep causal claims conditional when the evidence is not causal.
```

### Action list

```text
Use numbered actions with short verbs. Separate ordinary self-management from red-flag symptoms using coral only for the warning area. Do not turn general education into an individualized treatment plan.
```

## 纠错规则

中文错误时不要用代码覆盖位图。复制原提示词为新版本，只修改错误标签、减少文字或改为无文字主体图，再重新生成对应 `-v2.png`。成功图片不随失败项一起重做。
