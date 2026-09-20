# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，使智能体能在对话中自动识别并执行特定类型任务（如文件解析、数据清洗等），无需开发者编写集成代码或调用外部 API。官方 Skill 开箱即用，自定义 Skill 支持 ZIP 包上传，通过 `SKILL.md` 定义元信息与触发逻辑。其核心机制依赖 description 字段的语义描述质量来驱动智能体的自动调用决策。

## 支持的模型/功能

- **适用模型**：Skill 与百炼平台所有支持智能体（Agent）模式的大模型兼容，包括 Qwen 系列（如 qwen-max、qwen-plus）、以及接入的第三方模型（需启用 Agent 模式）。Skill 本身不绑定具体模型，而是由智能体运行时根据 `description` 的语义匹配动态选择调用。
- **功能范围**：当前仅支持**文件处理类任务**（如读取、编辑、生成、转换 `.xlsx`, `.csv`, `.pdf`, `.docx` 等格式），不支持纯文本生成、API 调用、数据库连接或长期状态维护等通用 Agent 功能。该限制在 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中明确界定为“以文件为输入/输出的确定性操作”。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，须全小写+连字符（如 `pdf-extractor`），同一账号下不可重复。详见 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 中“SKILL.md 编写规范”章节。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | 决定 Skill 是否被调用的核心字段。必须包含适用输入类型、支持操作、典型触发关键词及明确的**不适用场景**（例如：“Do NOT trigger when output is HTML”）。描述质量直接影响召回准确率，[原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 提供了完整示例和编写建议。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB，超限将直接拒绝上传。 |

> **注意**：文档中未提及 `version` 字段为必填项，且 `SKILL.md` 示例中也未出现该字段；但部分旧版控制台 UI 曾显示版本号。实际行为以 [原文标题](../../raw/application-user-guide/skill/introduction-to-skill.md) 为准：系统通过 ZIP 文件哈希或上传时间自动管理版本，`SKILL.md` 中无需声明 `version`。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面查看并添加，无需配置。  
   - 自定义 Skill：按规范编写 `SKILL.md`，打包为 ZIP（根目录含 `SKILL.md`，无嵌套文件夹），在控制台「组件 > Skill 管理 > 自定义 Skill」上传。

2. **添加到智能体**  
   - 方式一：从 Skill 详情页点击「添加到智能体」，选择目标应用；  
   - 方式二：进入智能体「应用配置」→「技能」区域，点击 `+` 号勾选所需 Skill。

3. **测试与验证**  
   在应用配置页右侧对话窗格中发送符合 `description` 触发条件的自然语言指令（如“把附件里的 CSV 按销售额排序并导出新表格”），观察是否自动调用并返回预期文件。

## 限制和注意事项

- **文件类型限制**：仅支持平台白名单内的文件格式（如 `.xlsx`, `.csv`, `.pdf`, `.docx`, `.txt`），不支持 `.exe`, `.zip`, `.bin` 等可执行或二进制非文档格式。上传非法格式 ZIP 包将导致审查失败。
- **无状态性**：每个 Skill 执行是独立的，不保留跨轮次上下文或临时文件。无法实现“先读取 A 表，再基于结果修改 B 表”的链式操作（需拆分为多个 Skill 或改用 Function Calling）。
- **审查延迟**：自定义 Skill 上传后需约 2 分钟自动审查，期间不可用；审查失败时需根据错误提示修改 `SKILL.md` 后重新上传。
- **版本更新逻辑**：重新上传同名 Skill ZIP 包即创建新版本，已添加该 Skill 的智能体会**自动切换至最新版本**（官方 Skill 同理）。旧版本不可回滚，历史版本仅用于查看（见「更新记录」标签）。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


