# Agent 兼容性

## 共同核心

跨 Agent 可移植部分是 `SKILL.md`、`references/` 和 `scripts/`。所有环境都必须遵守：保留原稿、健康风险扫描、一次确认、提示词先落盘、只用位图后端、失败项版本化重做、输出边界明确。

## Codex

- 安装：`/Users/mac/.codex/skills/jiaojie-health-illustrator/` 或对应 `$CODEX_HOME/skills/`。
- `agents/openai.yaml` 提供 Codex UI 名称、描述和默认提示词。
- 位图默认使用原生 `imagegen`，不需要用户提供 API Key。
- 原生工具生成后，把选定 PNG 移动或复制到发布包 `imgs/`；不要让文章引用只存在于 Codex 默认生成目录的文件。

## Claude Code

- 项目安装：`<project>/.claude/skills/jiaojie-health-illustrator/`。
- 个人安装：`~/.claude/skills/jiaojie-health-illustrator/`。
- Claude Code 读取 `SKILL.md` 和相对引用；`agents/openai.yaml` 是 Codex 元数据，可以忽略。
- 完整出图需要可调用的位图后端，例如 `baoyu-image-gen`、图像 MCP 工具或其他原生图像工具。
- 后端必须能生成或导出 PNG，并允许代理把结果保存到发布包目录。

## 后端选择

1. 当前请求明确指定的可用后端。
2. 当前 Agent 的原生位图工具。
3. 已安装且唯一可用的非原生位图后端。
4. 存在多个非原生后端时，一次性询问用户。

不得用 SVG、HTML、Canvas、CSS 或程序化绘图替代要求的位图配图。

## 没有位图后端

仍可交付：

- 文章结构分析；
- 健康风险与建议改写；
- 分级免责声明建议；
- `imgs/outline.md`；
- `imgs/prompts/*.md`。

必须明确写出：PNG 未生成、最终带图 Markdown 未完成、公众号 HTML 未完成、ZIP 未创建。不要制造空白 PNG、占位图片或伪造验证成功。

## 测试边界

v1 完整验证目标为 Codex。本 Skill 的文件结构和 Python 验证器可用于 Claude Code，但实际出图质量取决于其后端。Claude.ai 与 Claude API 的文件、网络和执行环境不同，不在 v1 的验证范围内。
