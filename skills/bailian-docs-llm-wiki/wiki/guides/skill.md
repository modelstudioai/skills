# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。它通过语义匹配自动触发，开发者可选用平台预置的官方 Skill，或按规范打包上传自定义 Skill。其核心机制依赖 `SKILL.md` 中的描述质量与模型对任务意图的理解能力，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 功能由百炼平台统一调度，当前所有支持智能体（Agent）模式的模型（如 Qwen-Max、Qwen-Plus、Qwen-Turbo）均可调用 Skill，无需模型侧额外适配。
- **核心能力类型**：
  - 文件处理类：如 `xlsx`、`pdf`、`docx` 等格式的读取、编辑、生成与转换；
  - 数据操作类：结构化数据清洗、行列计算、格式标准化；
  - 轻量工具类：如文本提取、表格识别、简单图表生成等。
- **不支持能力**：Skill 不提供长期状态维护、外部 API 主动调用（需通过 Function Calling 实现）、实时数据库写入或流式大文件处理。详细能力边界请参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定 Skill 是否被触发的关键字段，必须明确说明输入类型、支持操作、典型触发词及**明确排除的场景**（避免误调）。质量直接影响召回准确率。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB；超限将直接拒绝上传，不进入审查流程。 |
| `version` | 非显式字段 | 否 | 由平台自动生成（时间戳格式），自定义 Skill 每次重传同名包即创建新版本；官方 Skill 版本由平台统一管理。 |

> **注意**：`description` 字段虽为文本，但实际承担类似“提示工程接口”的作用——模型依据该描述做意图匹配，而非执行硬规则匹配。因此，[Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中强调的“触发关键词”和“不适用场景”必须用自然语言清晰表达，不可依赖正则或逻辑符号。

## 使用方式

1. **添加 Skill 到智能体**（二选一）：
   - 从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击目标 Skill 卡片 → “添加到智能体”；
   - 或在智能体应用的 **应用配置 → 技能** 区域，点击 `+` 号选择 Skill。
2. **验证触发逻辑**：
   - 在应用配置页右侧对话窗格中，使用贴近真实用户表达的指令测试（如：“把这份 CSV 里销售额列转成万元单位，并导出新表格”）；
   - 观察是否调用预期 Skill 并返回正确结果（如生成 `.xlsx` 文件）。
3. **更新自定义 Skill**：
   - 修改本地 ZIP 包内 `SKILL.md`（尤其优化 `description`）后，重新上传同名包；
   - 审查通过后，已绑定该 Skill 的智能体**自动切换至最新版本**，无需重新发布应用。

## 限制和注意事项

- **调用延迟**：Skill 执行属于异步后台任务，单次调用平均耗时 2–8 秒，超时阈值为 30 秒；超时后智能体将终止调用并返回失败提示。
- **文件限制**：
  - 单次处理文件数 ≤ 5 个；
  - 单个文件大小 ≤ 50 MB（PDF/DOCX/XLSX 等格式）；
  - 不支持加密文件、损坏文件或需交互式认证的云存储链接（如未授权的 OneDrive 直链）。
- **描述失配风险**：若 `description` 过于宽泛（如仅写“处理表格”）或遗漏关键排除项（如未声明“不处理含宏的 xlsm”），将导致高频误触发。务必遵循文档中的 [description 编写建议](../../raw/application-user-guide/skill/introduction-to-skill.md)。
- **调试建议**：当 Skill 未被触发时，优先检查 `description` 是否覆盖了测试语句中的动词（如“生成”“清洗”“转换”）和名词（如“.csv”“销售数据”“分列统计”），而非仅依赖关键词字面匹配。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


