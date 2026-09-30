# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，支持无需编码即可让智能体自动识别并执行特定类型任务（如文件解析、数据清洗、格式转换等）。官方 Skill 开箱即用，自定义 Skill 则通过 ZIP 包上传实现业务定制。其核心机制依赖 `SKILL.md` 中的语义描述驱动智能体调用决策，而非硬编码规则。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 `qwen-max`、`qwen-plus` 及后续标注支持 Skill 的模型），不依赖底层大模型自身是否具备工具调用原生能力，由平台统一调度层封装。
- **核心功能**：
  - 自动触发：基于用户输入语义与 `SKILL.md` 中 `description` 的匹配度判断是否调用；
  - 文件处理：官方 Skill 已覆盖 `.xlsx`、`.csv`、`.pdf`、`.docx` 等主流格式的读取、生成、转换与清洗；
  - 多版本管理：自定义 Skill 支持按名称覆盖上传新版本，已绑定应用自动生效；
  - 零代码集成：添加后无需修改智能体提示词或接入外部 API，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：部分旧版文档提及“仅 `qwen-max` 支持 Skill”，该说法已过时；实际支持范围以控制台 Skill 管理页的可用 Skill 列表为准，且平台会动态扩展支持模型——请以 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“官方 Skill 持续更新中”说明为最新依据。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，需全小写+连字符（如 `pdf-extractor`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | **决定调用准确性的关键字段**：必须明确输入类型、支持操作、触发关键词及不适用场景，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“description 编写建议”。 |
| ZIP 包大小 | 上传文件 | — | ≤ 10 MB，超限将被拒绝。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加；  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录含该文件），通过控制台「自定义 Skill」按钮上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」；  
   - 方式二：在目标智能体的「应用配置 → 技能」区域点击 `+` 添加。

3. **测试效果**  
   在应用配置页右侧对话窗格输入典型触发语句（如“把这份 CSV 按销售额排序并导出”），观察是否自动调用对应 Skill 并返回预期结果。

## 限制和注意事项

- **调用非确定性**：Skill 是否被触发取决于大模型对 `description` 语义的理解，非精确关键词匹配。描述模糊或覆盖场景过宽易导致误触发或漏触发。
- **无状态执行**：每个 Skill 调用均为独立会话，不共享上下文或临时文件；跨步骤任务（如“先清洗再绘图”）需确保单次描述完整涵盖全部操作。
- **文件输入限制**：当前仅支持用户上传的文件作为 Skill 输入源，不支持从 URL 或数据库直读；输出文件最大 50 MB。
- **版本兼容性**：自定义 Skill 更新后，已添加的应用立即使用新版本，但历史对话记录中的 Skill 执行仍按当时版本快照运行。
- **调试建议**：若 Skill 未触发，优先检查 `description` 是否遗漏关键触发词或误写了不适用场景；可参考官方 xlsx Skill 的 [完整示例](../../raw/application-user-guide/skill/introduction-to-skill.md) 进行对标优化。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


