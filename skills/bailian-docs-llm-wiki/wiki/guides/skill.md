# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行文件处理、数据分析等专业任务。官方 Skill 由平台预置并持续更新，自定义 Skill 则允许开发者通过 ZIP 包注入业务专属逻辑。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体调用决策，而非硬编码规则。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“添加 Skill 后，智能体可以在对话中自动识别匹配的任务”为准）。
- **核心功能**：
  - 自动触发：基于用户输入语义与 `SKILL.md` 中 `description` 的匹配度判断是否调用；
  - 文件处理：覆盖 `.xlsx`, `.csv`, `.tsv`, `.xlsm` 等格式的读取、编辑、生成与转换；
  - 数据操作：支持清洗、结构化、公式计算、图表生成等；
  - 多版本管理：官方 Skill 自动更新，自定义 Skill 通过同名 ZIP 重传实现版本迭代。

> **注意**：文档未明确说明 Skill 是否支持非表格类文件（如 PDF 解析、图像 OCR），亦未提及对流式输入或大文件分块处理的支持。实际能力边界请以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“官方 Skill 持续更新中”及控制台实时列表为准。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，需小写英文+连字符（如 `invoice-parser`），不可与账号下已有 Skill 重名 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定调用准确率的核心字段；必须包含输入类型、支持操作、触发关键词、不适用场景四要素（详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“description 编写建议”） |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限将导致审查失败 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录含该文件），在控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在目标应用「应用配置 > 技能」区域点击加号选择 Skill。

3. **测试效果**  
   在应用配置页右侧对话窗格输入典型指令（如“帮我清洗附件中的 CSV 表格”），观察是否触发 Skill 并返回预期文件。

## 限制和注意事项

- **ZIP 包限制**：仅接受单个 ZIP 文件，不支持嵌套 ZIP 或外部依赖下载；`SKILL.md` 必须位于根目录且严格使用 `---` 包裹 YAML。
- **调用可靠性**：`description` 描述质量直接影响触发准确率；模糊或缺失“不适用场景”易导致误调用（例如将 Word 生成需求错误匹配至 xlsx Skill）。
- **版本行为差异**：官方 Skill 更新后，已添加的应用**自动生效新版本**；自定义 Skill 需手动重传 ZIP 才能升级，旧版本仍保留在历史记录中供回溯。
- **审查耗时**：上传后约 2 分钟完成内容审查，失败时需根据提示修改 `SKILL.md` 后重试。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


