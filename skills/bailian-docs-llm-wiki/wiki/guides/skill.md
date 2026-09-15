# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。通过自然语言描述触发条件与能力边界，智能体可在对话中自动识别并调用匹配的 Skill 执行任务。官方 Skill 开箱即用，自定义 Skill 则通过 ZIP 包形式灵活适配业务场景，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：Skill 与底层大模型解耦，所有支持智能体应用的模型（如 Qwen 系列、Qwen2 系列）均可调用 Skill，无需模型侧特殊适配。
- **核心功能**：
  - 自动识别用户意图并匹配 Skill（基于 `SKILL.md` 中的 `description` 字段语义理解）；
  - 支持文件输入/输出（如 `.xlsx`, `.csv`, `.pdf`, `.docx` 等格式的读写、转换、清洗）；
  - 支持结构化数据操作（行列计算、格式化、图表生成、脏数据修复）；
  - 不支持非文件类外部服务调用（如数据库直连、HTTP API 调用、实时系统集成），此类能力需通过 Function Calling 或插件机制实现。

> **注意**：原始文档中“支持文件处理、数据分析等专业能力”表述较宽泛；实际能力严格受限于 Skill ZIP 包内实现的 Python 逻辑及百炼沙箱环境权限。例如，[Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 明确说明自定义 Skill 无法执行 Google Sheets API 集成或数据库管道任务——这些属于平台明确排除的场景。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，全账号范围内不可重复；仅支持小写字母、数字、连字符（`-`），长度 ≤ 64 字符。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定智能体是否调用该 Skill 的核心依据。必须包含适用输入类型、支持操作、典型触发关键词、不适用场景四要素，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 示例。 |
| `version` | `SKILL.md`（可选） | 否 | 若未声明，平台自动生成语义版本（如 `1.0.0`）；手动指定时需符合 SemVer 规范，用于版本管理与回滚。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加，无需配置。  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（≤10 MB），通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击 Skill 右侧 `+` 号添加。

3. **测试调用**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的请求（如“把附件里的 CSV 按销售额降序排列并导出为 Excel”），观察 Skill 是否被调用及输出是否符合预期。

## 限制和注意事项

- **沙箱限制**：所有 Skill 运行于隔离 Python 沙箱，禁用 `os.system`、`subprocess`、网络外连（除百炼内置文件服务外）、持久化磁盘写入等高危操作。
- **版本更新**：重新上传同名 ZIP 包将创建新版本，已添加该 Skill 的智能体**自动切换至最新版本**（官方 Skill 强制同步，自定义 Skill 同步策略相同）。
- **调试建议**：若 Skill 未被调用，优先检查 `description` 是否覆盖用户实际表达（如是否遗漏口语化触发词），而非修改代码逻辑；可参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的完整 description 示例优化表述。
- **命名冲突**：同一账号下 `name` 字段全局唯一，上传重名 Skill 将被拒绝，错误提示明确指向 `SKILL.md` 中的 `name` 值。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


