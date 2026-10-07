# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力单元，支持无需编码即可为智能体赋予文件处理、数据分析等专业功能。通过语义化描述驱动自动调用，Skill 分为平台预置的官方 Skill 和用户自主开发的自定义 Skill 两类。其核心机制依赖于 `SKILL.md` 中的精准描述来匹配用户意图，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼大模型（如 Qwen 系列最新推理模型），具体兼容性以控制台 Skill 管理页实时列表为准。
- **核心功能**：
  - 自动识别用户对话中的任务意图并触发对应 Skill；
  - 支持文件输入/输出（如 `.xlsx`, `.csv`, `.pdf`, `.docx` 等格式的读取、生成、转换、清洗）；
  - 官方 Skill 覆盖通用办公与数据场景；自定义 Skill 可扩展至行业专属逻辑（如发票解析、医疗报告结构化）；
  - 版本化管理：官方 Skill 自动更新，自定义 Skill 通过同名 ZIP 重上传实现版本迭代。

> **注意**：部分旧版文档提及“Skill 仅支持 Qwen-1.5-72B”，该说法已过时；当前 v2.0+ 智能体运行时已统一支持全量 Qwen 推理模型，以 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“添加 Skill 后，智能体在对话中遇到匹配 Skill 描述的任务时，会自动调用该 Skill 执行处理”为准。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，需小写英文+连字符（如 `invoice-parser`），不可与账号下已有 Skill 重名。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定调用准确率的核心字段，必须明确包含：输入类型、支持操作、典型触发关键词、**不适用场景**（避免误触发）。参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx 示例的完整结构。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限将被拒绝。 |
| `SKILL.md` 存在性 | ZIP 根目录 | 是 | 缺失则审查失败，无例外。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”；  
   - 自定义 Skill：编写符合规范的 `SKILL.md`，打包为 ZIP（根目录含该文件），在控制台 **组件 > Skill 管理 > 自定义 Skill** 中上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击 **添加到智能体**，选择目标应用；  
   - 方式二：进入智能体 **应用配置 > 技能** 区域，点击 Skill 右侧 `+` 号添加。

3. **测试调用**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的指令（如“把附件里的 CSV 按销售额排序并导出为 Excel”），观察是否自动调用并返回预期文件。

## 限制和注意事项

- **调用限制**：单次对话中 Skill 调用次数受智能体配额约束，高频调用需申请提升额度；
- **文件限制**：单个输入文件 ≤ 50 MB，输出文件 ≤ 100 MB；ZIP 包本身 ≤ 10 MB；
- **描述质量强相关**：`description` 若未明确排除不适用场景（如“不产出 HTML 报告”），可能导致误触发——这是当前 Skill 失败的最主要原因；
- **版本生效逻辑**：官方 Skill 更新后，已添加的应用**立即生效**；自定义 Skill 更新需重新上传，且已添加的应用**自动切换至最新版本**（无需手动刷新）；
- **调试建议**：若 Skill 未被调用，优先检查 `description` 是否覆盖用户实际表述（如口语化路径：“我桌面上那个 sales.xlsx”），而非仅依赖技术术语。

> **注意**：原始文档中“审查预计耗时约 2 分钟”为历史基准值，当前生产环境平均审查时间已优化至 < 30 秒，但极端复杂 ZIP（如含大量嵌套脚本）仍可能延长，以控制台实际提示为准。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


