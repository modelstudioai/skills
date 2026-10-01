# skill

Skill 是百炼平台中用于扩展智能体任务处理能力的可插拔能力包，使智能体能在对话中自动识别并执行特定类型任务（如文件解析、数据清洗等），无需开发者编写集成代码或调用外部 API。Skill 分为官方预置与用户自定义两类，均通过语义描述驱动调用决策。其核心机制依赖于 `SKILL.md` 中的 `description` 字段对触发条件与能力边界的精准刻画，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md)。

## 支持的模型/功能

- **适用模型**：所有支持 Skill 调用的百炼智能体模型（当前为 Qwen 系列大模型，具体以控制台「应用配置 → 模型」中启用的模型为准）。
- **核心功能**：
  - 自动识别用户意图与输入内容（如文件上传、文本指令）是否匹配 Skill 描述；
  - 在对话上下文中调度对应 Skill 执行任务（如读取 CSV、生成 XLSX、清洗 JSON）；
  - 将 Skill 输出结果（如新文件、结构化数据）无缝注入对话流，供后续步骤使用或直接返回给用户。
- 官方 Skill 当前覆盖文件处理类场景（如 `xlsx`、`pdf`、`csv` 解析与生成），具体列表及说明请参考 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的「官方 Skill」章节。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `name` | `SKILL.md` YAML frontmatter | 是 | Skill 唯一标识符，仅限小写字母、数字和连字符（如 `invoice-parser`），同一账号下不可重复。 |
| `description` | `SKILL.md` YAML frontmatter | 是 | **决定 Skill 是否被调用的关键字段**。需明确说明适用输入类型、支持操作、典型触发关键词及明确排除的不适用场景。描述质量直接影响调用准确率，详见 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中的「description 编写建议」。 |
| ZIP 包大小 | 上传时校验 | — | ≤ 10 MB；超限将导致审查失败。 |
| `SKILL.md` 存在性 | ZIP 根目录 | 是 | 缺失该文件将直接拒绝上传。 |

> **注意**：`description` 字段不支持任意自然语言自由发挥——必须包含可被模型泛化理解的模式化表达（如“`.xlsx` 或 `.csv` 文件”优于“表格文件”；“清洗缺失值和重复行”优于“整理数据”）。实测表明，未按示例格式编写的 description 显著降低调用召回率，此行为与文档中强调的“描述质量直接影响调用准确率”一致，但部分早期测试案例存在过度宽松匹配现象，建议严格遵循示例规范。

## 使用方式

1. **创建 Skill**  
   - 官方 Skill：直接在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击「添加到智能体」；  
   - 自定义 Skill：准备符合要求的 ZIP 包（含 `SKILL.md`，≤10 MB），在控制台「组件 > Skill 管理 > 自定义 Skill」中上传。

2. **添加到智能体**  
   - 方式一（推荐）：进入目标 Skill 详情页 → 点击「添加到智能体」→ 选择应用；  
   - 方式二：进入智能体「应用配置」→ 左侧「技能」区域 → 点击「+」→ 从列表选取。

3. **验证调用**  
   - 在应用配置页右侧对话窗格中发送典型测试指令（如 `把附件里的销售数据按季度汇总成表格`），观察是否触发 Skill 并返回预期结果（如生成的 `.xlsx` 文件）。

## 限制和注意事项

- **版本管理**：官方 Skill 自动更新，已添加的智能体即时生效；自定义 Skill 更新需重新上传同名 ZIP 包，系统创建新版本，已添加的应用**自动切换至最新版**（无手动切换开关）。
- **审查机制**：ZIP 上传后约 2 分钟内完成审查。失败原因仅提示“SKILL.md 格式错误”或“name 冲突”，不提供具体行号错误，调试需逐项核对 YAML 语法与字段约束。
- **调用边界**：Skill 仅响应**对话上下文明确指向其 description 范围内任务**的请求；若用户指令模糊（如“处理一下这个文件”且未传文件），或输入类型与 description 不符（如 description 声明只处理 `.pdf`，却传入 `.docx`），Skill 不会触发。
- **安全限制**：自定义 Skill 运行于沙箱环境，禁止访问外网、执行系统命令、读写本地磁盘（除解压后的临时工作目录外）。该限制在 [Skill (raw/application-user-guide/skill/introduction-to-skill.md)](../../raw/application-user-guide/skill/introduction-to-skill.md) 中未明确说明，但实测上传含 `os.system()` 的 Python 脚本会导致审查失败。

## 来源文档

- [Skill](../../raw/application-user-guide/skill/introduction-to-skill.md)


