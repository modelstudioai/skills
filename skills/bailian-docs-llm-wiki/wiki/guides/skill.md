# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，使智能体能在对话中自动识别并执行特定类型任务（如文件解析、数据清洗等），无需开发者编写集成代码或调用外部 API。Skill 分为官方预置与用户自定义两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件、输入约束和输出要求的精准刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体以控制台「应用配置 → 模型」中启用的模型为准）。
- **核心功能**：
  - 自动识别用户意图与 Skill 描述的语义匹配度；
  - 基于文件输入（如 `.xlsx`, `.csv`, `.pdf` 等）执行格式转换、内容提取、结构化清洗等操作；
  - 输出结果可为新文件（如生成 `.xlsx`）、结构化 JSON 或文本摘要；
  - 官方 Skill（如 `xlsx`, `pdf`, `csv`）开箱即用；自定义 Skill 需符合 ZIP 包规范。

> **注意**：部分旧版文档提及 Skill 可直接调用 Python 函数或 HTTP 接口，但根据最新实现，Skill **不执行任意代码**，仅通过平台内置运行时处理文件与结构化数据——该能力边界已在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中明确限定。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 全局唯一标识符，仅支持小写字母、数字、连字符（如 `invoice-parser`）；重复名称将导致上传失败。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定 Skill 是否被调用的核心字段。必须包含：输入类型（如 `.pdf`）、支持操作（如“提取表格”）、典型触发词（如“帮我转成 Excel”）、**明确排除场景**（如“不处理扫描件文字识别”）。质量直接影响召回率与准确率。 |
| ZIP 包大小 | 上传文件 | — | ≤ 10 MB；超限将被拒绝，审查不通过提示为 `file too large`。 |

`description` 编写质量至关重要，建议严格参照 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的完整示例组织内容。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面直接添加；  
   - 自定义 Skill：准备含合规 `SKILL.md` 的 ZIP 包，通过「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：进入目标应用「应用配置」→「技能」区域 → 点击 `+` 选择 Skill。

3. **测试调用**  
   在应用配置页右侧对话窗格输入典型用户指令（如 `把附件里的销售表按季度汇总`），观察是否触发 Skill 并返回预期文件。

## 限制和注意事项

- **版本管理**：官方 Skill 自动更新，已添加的应用即时生效；自定义 Skill 更新需重新上传同名 ZIP，系统创建新版本，**已有应用不会自动切换**，需手动在应用配置中确认升级。
- **文件限制**：Skill 处理的单个输入文件最大为 50 MB（PDF 文本提取）、10 MB（Excel/CSV 行数上限约 10 万行），超出将报错 `input file too large`。
- **描述歧义风险**：若多个 Skill 的 `description` 存在重叠（如均声明支持“清洗 CSV”），智能体可能随机选择其一。应通过强化排除条款（如 `Do NOT trigger for files with >100 columns`）降低冲突概率。
- **调试建议**：若 Skill 未被调用，优先检查 `description` 是否缺失触发关键词、是否遗漏不适用场景说明，并验证 ZIP 包根目录是否存在且格式正确的 `SKILL.md`。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


