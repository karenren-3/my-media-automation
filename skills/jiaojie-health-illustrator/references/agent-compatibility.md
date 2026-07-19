# Agent 兼容性

## 共同核心

跨 Agent 可移植部分是 `SKILL.md`、`references/` 和 `scripts/`。所有环境都必须遵守：保留原稿、健康风险扫描、一次确认、提示词先落盘、只用位图后端、失败项版本化重做、输出边界明确。

## Codex

- 安装：`/Users/mac/.codex/skills/jiaojie-health-illustrator/` 或对应 `$CODEX_HOME/skills/`。
- `agents/openai.yaml` 提供 Codex UI 名称、描述和默认提示词。
- 位图默认使用原生 `imagegen`，不需要用户提供 API Key。
- 原生工具生成后，把选定 PNG 移动或复制到发布包 `imgs/`；不要让文章引用只存在于 Codex 默认生成目录的文件。

## Claude Code

> **重点限制：Claude Code 没有 Codex 原生 `imagegen`。仅安装本 Skill 不等于具备出图能力。** 未另外配置位图后端时，Claude Code 只能完成健康表述核查、配图提纲和提示词文件，不能生成 PNG，也不能把任务描述为“完整公众号配图发布包”。

- 项目安装：`<project>/.claude/skills/jiaojie-health-illustrator/`。
- 个人安装：`~/.claude/skills/jiaojie-health-illustrator/`。
- Claude Code 读取 `SKILL.md` 和相对引用；`agents/openai.yaml` 是 Codex 元数据，可以忽略。
- 完整出图需要可调用的位图后端，例如 `baoyu-image-gen`、图像 MCP 工具或其他原生图像工具。
- 后端必须能生成或导出 PNG，并允许代理把结果保存到发布包目录。
- 上传微信公众号草稿箱还需要单独安装 `baoyu-post-to-wechat`，并具备 Bun、Chrome 和已登录的公众号会话。Claude Code 本身不会提供这些登录状态或发布权限。
- 如果自动保存无法独立验证，必须停在已填充的编辑页让用户手动保存；不得把用户手动保存描述成自动保存成功。

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

完整验证目标为 Codex。本 Skill 的文件结构和 Python 验证器可用于 Claude Code，但实际出图质量取决于其后端。Claude.ai 与 Claude API 的文件、网络和执行环境不同，不在当前验证范围内。
