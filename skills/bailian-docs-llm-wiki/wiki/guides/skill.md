# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔功能单元，支持无需编码即可为智能体赋予文件解析、数据处理等专业能力。它通过语义描述驱动自动调用，适用于官方预置场景与业务定制需求。详细背景见 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **官方 Skill**：由平台统一维护，覆盖常见文件处理任务（如 `.xlsx`、`.csv` 解析与生成、PDF 文本提取、图像 OCR 等），添加后即刻可用，版本自动同步。
- **自定义 Skill**：通过 ZIP 包上传实现，支持任意 Python 逻辑封装（需符合运行时约束），适用于行业专属格式解析、私有 API 集成等场景。ZIP 包必须包含符合规范的 `SKILL.md` 元信息文件，详见 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)。

> **注意**：当前所有 Skill 均运行于隔离沙箱环境，**不支持**访问外部网络、持久化存储或系统级调用；自定义 Skill 的 Python 依赖须全部打包进 ZIP，且仅支持纯 Python 模块（不含 C 扩展）。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定智能体是否触发该 Skill 的核心依据。需明确输入类型、支持操作、典型触发词及**排除场景**（避免误调用）。示例见 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md) 中 xlsx Skill 的完整描述。 |
| ZIP 包大小 | 上传文件 | — | ≤ 10 MB，超限将被拒绝。 |

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择添加。  
   - 自定义 Skill：按 [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md) 要求编写 `SKILL.md`，打包 ZIP 后上传至控制台「组件 > Skill 管理 > 自定义 Skill」。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用。  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击对应 Skill 右侧的 `+` 添加。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送典型用户指令（如 `把附件里的销售表按季度汇总并生成图表`），观察是否正确触发 Skill 并返回预期结果（如 `.xlsx` 文件下载链接）。

## 限制和注意事项

- **版本更新行为差异**：官方 Skill 更新后，已添加的应用**自动生效最新版本**；自定义 Skill 更新需重新上传同名 ZIP，且**已添加的应用不会自动切换版本**，需手动在应用配置中确认启用新版本。
- **触发准确性依赖 description 质量**：若 `description` 未明确排除不适用场景（如“不处理 Word 文档”），可能导致误调用。强烈建议按文档要求覆盖输入类型、操作、触发词、排除项四要素。
- **沙箱限制**：自定义 Skill 运行于无网络、无磁盘写入、无进程派生的受限环境，超时默认为 60 秒（不可配置），内存上限为 1 GB。
- **调试支持有限**：审查失败时仅提示 `SKILL.md` 格式或字段缺失问题，不提供运行时日志；建议本地使用 `bailian-skill-tester` CLI 工具预验证（参见 SDK 文档）。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


