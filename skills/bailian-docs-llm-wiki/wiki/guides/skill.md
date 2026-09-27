# skill

Skill 是百炼平台提供的可插拔能力包，用于赋予智能体自动处理特定任务（如文件解析、数据清洗等）的能力，无需开发者编写额外代码或集成外部工具。通过官方 Skill 或自定义 ZIP 技能包，智能体可在对话中基于语义理解自动识别任务并调用对应 Skill 执行。该机制依赖 `SKILL.md` 中的 `description` 字段进行触发判断，因此描述质量直接影响调用准确性。

## 支持的模型/功能

Skill 本身不绑定特定大模型，而是作为独立于模型推理层的执行单元，在智能体决策链中被动态调用。当前支持两类 Skill：

- **官方 Skill**：由平台预置并统一维护，覆盖常见场景（如 `xlsx`、`pdf`、`csv` 处理），添加后即刻可用，且已添加的智能体会自动升级至最新版本。最新列表请参考 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面。
- **自定义 Skill**：通过上传符合规范的 ZIP 包创建，适用于官方未覆盖的业务需求（如行业专用格式解析）。ZIP 包必须包含根目录下的 `SKILL.md` 文件，并满足[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)中定义的元信息与结构要求。

> **注意**：官方 Skill 的更新策略与自定义 Skill 不同——前者自动生效，后者需手动重新上传 ZIP 包触发版本更新；二者在控制台中分属不同标签页管理，不可混用配置入口。

## 关键参数

所有 Skill 的行为核心由 `SKILL.md` 中的 YAML frontmatter 控制，关键字段如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | Skill 唯一标识符，仅支持小写字母、数字和连字符（如 `invoice-parser`），且在同一账号下不可重复。该名称将用于系统内部引用和日志追踪。 |
| `description` | 是 | **决定 Skill 是否被调用的核心依据**。需明确说明适用输入类型、支持操作、典型触发关键词及明确排除的不适用场景。描述质量直接影响智能体调用准确率，详见[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)中的编写建议与完整示例。 |

ZIP 包整体大小不得超过 10 MB，超出将导致审查失败。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”即可。  
   - 自定义 Skill：按[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)所述，准备含合规 `SKILL.md` 的 ZIP 包，进入“组件 > Skill 管理 > 自定义 Skill”上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击“添加到智能体”，选择目标应用；  
   - 方式二：在目标智能体的“应用配置 > 技能”区域，点击 Skill 右侧加号添加。

3. **测试效果**  
   添加后，可在应用配置页右侧对话窗格中发送典型用户指令（如“帮我清洗这个 CSV 中的空行和重复列”），观察是否正确触发 Skill 并返回预期结果（如下载清洗后的文件）。

## 限制和注意事项

- **版本管理差异**：官方 Skill 更新由平台后台静默完成，已添加的应用自动使用新版；自定义 Skill 必须重新上传同名 ZIP 包才能生成新版本，旧版本不会被覆盖，历史版本可通过详情页“概览”标签切换查看。
- **触发依赖描述质量**：`description` 中若未清晰界定适用/不适用边界（例如遗漏“不适用于生成 HTML 报告”），可能导致误触发。强烈建议严格遵循[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md)中列出的四项描述要素编写。
- **审查耗时**：自定义 Skill 上传后需约 2 分钟完成内容审查，审查失败时需根据控制台提示修改 `SKILL.md` 后重试。
- **命名唯一性约束**：同一账号下 `name` 字段全局唯一，重复上传将被拒绝，而非覆盖。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


