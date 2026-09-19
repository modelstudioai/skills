# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，使智能体能在对话中自动识别并执行特定类型任务（如文件解析、数据清洗等），无需开发者编写集成代码或调用外部 API。Skill 分为官方预置与用户自定义两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件、输入输出和边界场景的精确刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼大模型（当前为 Qwen 系列 2.5 及以上版本），具体兼容性以控制台 Skill 管理页显示为准。
- **核心功能**：
  - 自动识别用户意图与 Skill 描述匹配度，触发调用；
  - 支持文件上传、解析、生成、格式转换等 I/O 操作（如 xlsx、csv、pdf、docx 等）；
  - 官方 Skill 提供开箱即用能力（如 `xlsx`、`pdf-extractor`、`csv-cleaner`）；
  - 自定义 Skill 支持 ZIP 包封装任意 Python 逻辑（需符合运行时沙箱约束）。

> **注意**：部分旧版文档提及“Skill 可调用任意 HTTP 接口”，该描述已过时；当前自定义 Skill 运行于隔离沙箱中，**不支持网络外连**，仅可通过内置 SDK 访问百炼平台提供的文件系统与基础工具链。请以 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“上传并创建”章节的运行环境说明为准。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，须小写英文+连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定调用准确性的关键字段，需明确输入类型、支持操作、触发关键词及**不适用场景**（避免误触发）。示例见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的完整描述。 |
| `version` | `SKILL.md`（可选） | 否 | 若未声明，系统自动生成时间戳版本号；建议显式声明便于追踪。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面添加；  
   - 自定义 Skill：打包含 `SKILL.md` 的 ZIP（≤10 MB），通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在目标应用的「应用配置 > 技能」区域点击 `+` 添加。

3. **测试与验证**  
   - 在应用配置页右侧对话窗格输入典型触发语句（如“把附件里的 CSV 按销售额排序并导出 Excel”）；  
   - 观察是否自动调用对应 Skill 并返回预期结果（如生成 .xlsx 文件）。

## 限制和注意事项

- **大小限制**：ZIP 包总大小 ≤ 10 MB；解压后文件数建议 ≤ 100 个，避免加载超时。
- **运行时限制**：自定义 Skill 运行在无网络、无持久存储的轻量沙箱中，单次执行超时为 60 秒，内存上限 1 GB。
- **版本管理**：重新上传同名 ZIP 即创建新版本；已添加该 Skill 的智能体会**自动升级至最新通过审查的版本**（官方 Skill 强制同步，自定义 Skill 需手动重传）。
- **调试提示**：若 Skill 未被调用，请优先检查 `description` 是否覆盖用户实际表达（如缺少口语化触发词）、输入文件类型是否在声明范围内，以及 ZIP 结构是否合规（`SKILL.md` 必须位于根目录）。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


