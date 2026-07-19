# 交付包契约

## 目录结构

每篇文章使用一个独立目录，ZIP 放在主题目录旁边：

```text
公众号发布包/
├── <文章主题>/
│   ├── imgs/
│   │   ├── outline.md
│   │   ├── prompts/
│   │   │   ├── 01-<type>-<slug>.md
│   │   │   └── ...
│   │   ├── 01-<type>-<slug>.png
│   │   └── ...
│   ├── <文章主题>_文章源稿.md
│   └── <文章主题>_公众号可复制版.html
└── <文章主题>_公众号发布包.zip
```

原始输入留在原位置，不放进发布 ZIP。若输入是粘贴文本，把原始粘贴内容另存为工作副本，但不要把后续改写覆盖到该副本。

## 生成顺序

1. 记录原始文件哈希。
2. 创建主题目录和 `imgs/outline.md`。
3. 保存全部 `imgs/prompts/*.md`。
4. 从已保存提示词生成同编号 PNG。
5. 创建派生 Markdown，并在相应段落后插入相对路径：

   ```markdown
   ![描述](imgs/01-comparison-example.png)
   ```

6. 生成本地公众号可复制 HTML，解析真实图片路径，不执行登录、提交或群发。
7. 验证主题目录。
8. 验证通过后创建 ZIP。
9. 再次计算原始文件哈希并确认不变。

## 命名与一致性

- 编号从 `01` 开始，按文章阅读顺序递增。
- PNG 与提示词必须共享编号、类型和 slug。
- 默认 PNG、提示词和 Markdown 图片引用均为 3–5 个且数量相同。
- `outline.md` 中的文件名必须与实际 PNG 一致。
- HTML 不能残留 `WECHATIMGPH_*`，所有本地 `<img src>` 必须存在。
- 失败候选使用 `-v2` 等版本名；最终 Markdown 和 HTML 只引用选定版本。

## 原稿哈希

macOS 可使用：

```bash
shasum -a 256 "/absolute/path/to/source.docx"
```

Linux 可使用：

```bash
sha256sum "/absolute/path/to/source.docx"
```

把开始和结束的哈希写入工作记录；两者必须相同。对粘贴内容，则对首次保存的只读工作副本做同样检查。

## 验证命令

从 Skill 目录运行：

```bash
python3 scripts/validate_package.py "/absolute/path/to/公众号发布包/<文章主题>"
```

用户覆盖数量或比例时传入实际值：

```bash
python3 scripts/validate_package.py "/absolute/path/to/package" --min-images 2 --max-images 2 --ratio 1:1
```

只有输出 `PACKAGE_OK` 才能创建最终 ZIP 并称为“完整发布包”。验证器检查：核心文件、PNG 数量、提示词数量、Markdown 图片数、PNG 比例、HTML 占位标记和本地图片引用。

## 局部交付覆盖

用户明确要求“只生成图片”或“不要 HTML/ZIP”时，可以缩小交付范围。报告中必须写清未生成项；不要运行完整发布包验证，也不要把局部交付称为完整发布包。

## 可选草稿箱上传

草稿箱上传不改变本地交付包结构，也不是 `PACKAGE_OK` 的必要条件。只有用户明确要求时才执行，并在本地包验证通过后开始。

发布报告必须区分：

- `自动保存成功`：保存动作由代理发起，且后台返回可验证的草稿结果；
- `用户手动保存成功`：用户在已填充编辑器中点击保存并确认；
- `保存未验证`：没有可靠的草稿结果。

用户手动介入后出现 `appmsgid`，只能报告“用户手动保存成功”，不能倒推为自动保存成功。
