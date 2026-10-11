# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行文件处理、数据分析等专业任务。Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，直接影响调用准确率——详情见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前包括 Qwen-Max、Qwen-Plus、Qwen-Turbo 等），具体兼容性以控制台 Skill 配置页实时提示为准。
- **核心功能**：
  - 自动识别用户意图与输入内容（如文件上传、关键词、操作请求）并匹配 Skill；
  - 执行文件解析、转换、生成、清洗等操作（如 `.xlsx`、`.csv`、`.pdf` 处理）；
  - 返回结构化结果或生成文件供下载；
  - 官方 Skill 支持开箱即用；自定义 Skill 支持 ZIP 包形式封装逻辑（含 Python 脚本、依赖声明等，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)）。

> **注意**：部分旧版文档提及“Skill 仅支持 Qwen-Max”，该说法已过时；实际自 v2024.06 起，所有主流推理模型均已支持 Skill 调用能力，以控制台最新说明为准。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，需小写英文+连字符（如 `pdf-merger`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | **决定调用准确性的关键字段**：必须明确输入类型、支持操作、典型触发词及明确排除场景（参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx 示例）。 |
| `version` | `SKILL.md`（可选） | 否 | 若未声明，系统自动生成时间戳版本号；建议显式声明便于追踪。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB；超限将直接拒绝上传。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面直接启用；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录含该文件），通过控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：在智能体「应用配置 > 技能」区域点击 `+`，勾选所需 Skill。

3. **测试与验证**  
   - 在应用配置页右侧对话窗格中发送典型请求（如 `把附件里的 CSV 按销售额排序并导出 Excel`），观察是否触发对应 Skill 并返回预期结果。

## 限制和注意事项

- **调用限制**：单次对话中 Skill 调用次数上限为 3 次（防循环调用），超出后智能体将终止 Skill 相关流程并返回提示。
- **文件限制**：Skill 可处理的单个输入文件大小上限为 50 MB；超过此值将被拒绝处理。
- **描述质量强相关**：`description` 若未清晰界定适用/不适用场景（如遗漏“不适用于数据库直连”），极易导致误触发或漏触发——务必严格遵循 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的编写建议。
- **版本更新**：官方 Skill 更新后自动生效；自定义 Skill 需重新上传同名 ZIP 包以发布新版本，历史版本保留在详情页「更新记录」中可追溯。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


