# 函数调用

函数调用（Function Calling）是百炼平台中让大模型在推理过程中**自主识别用户意图、生成结构化工具请求，并安全执行外部能力**的核心机制。它不是简单的 API 转发，而是模型基于语义理解主动决策“何时调用、调用哪个、传什么参数”的闭环过程，支撑智能体实现文件处理、实时搜索、代码执行、图像生成等超越纯语言生成的复合任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台以三种形态落地，面向不同开发粒度和控制需求：

- **Managed Agents（托管智能体）**：通过 Skill 注册自定义函数（HTTP 或内部服务），Agent 在会话中自动触发调用；`tool_choice` 参数控制策略（`"auto"`/`"none"`/指定 Skill ID），调用事件（如 `tool_call_started`）可通过 Webhook 实时监听。
- **Application Component API（应用组件）**：在 `/v1/applications/{app_id}/chat/completions` 请求中，通过 `tools` 数组声明函数 schema，配合 `tool_choice: "auto"` 启用自动调用；模型返回 `tool_calls` 字段，含 `function.name` 和 `function.arguments`（JSON 字符串），需开发者自行解析并执行。
- **Plug-in（插件）与 Skill（技能）**：  
  - *插件*：面向通用能力（如 `calculator`、`text_to_image`），通过 `tool_id` 显式标识，支持 Header/Query/Bearer 等鉴权方式，输入参数需严格按 `SKILL.md` 或插件配置定义；  
  - *Skill*：面向文件与数据操作（如 CSV 清洗、Excel 公式计算），依赖 `SKILL.md` 中 `description` 的语义匹配触发，无需显式命名调用，但要求 ZIP 包内规范定义输入/输出行为。

> ✅ 统一原则：所有场景下，函数调用均由模型**主动发起**，开发者负责提供清晰的函数描述（schema 或 description）、安全执行函数逻辑、并将结果按约定格式返回给模型继续推理。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 示例值 |
|------|----------|------|--------|
| `tool_choice` | Managed Agents / Application Component | 控制调用策略 | `"auto"`（默认）、`"none"`、`{"type": "function", "function": {"name": "calculator"}}` |
| `tools` | Application Component / Assistant API | 声明可用函数的 OpenAPI-like schema 数组 | `[{"type": "function", "function": {"name": "search_web", "description": "...", "parameters": {...}}}]` |
| `tool_id` | Plug-in | 插件内具体工具的唯一标识符，必须显式传递 | `"quark_search"`, `"code_interpreter"` |
| `name` | Skill | `SKILL.md` 中定义的 Skill 唯一标识，小写+连字符 | `"csv-cleaner"` |
| `description` | Skill / Plug-in | 决定是否触发调用的核心语义描述字段，需包含输入类型、支持操作、触发词、不适用场景 | `"清洗上传的 CSV 文件：去除空行、标准化列名、处理缺失值。不支持 Excel 或 JSON 格式。"` |

> ⚠️ 注意：`function.arguments` 始终为 JSON 字符串（非对象），需 `JSON.parse()` 后使用；所有参数值必须符合 schema 定义的类型与约束，否则调用将失败。

## 面向开发者，简洁实用

- **不要硬编码调用逻辑**：模型负责“判断要不要调”，你负责“确保能正确执行”。把精力放在写准 `description`、定义好 `parameters`、验证好函数返回格式上。
- **调试优先级**：  
  1. 检查 `description` 是否覆盖典型用户表达（如“画一只猫” vs “生成猫咪图片”）；  
  2. 验证 `parameters` 中 Object 类型的子属性是否全部填写（空属性会导致 Skill 审查失败）；  
  3. 确保函数返回结果是模型可理解的简洁文本或结构化 JSON（避免原始二进制、长日志）。
- **安全底线**：  
  - 自定义函数/插件必须做输入校验与沙箱隔离（尤其 `code_interpreter` 不允许外网访问）；  
  - 敏感凭证（如 API Key）务必通过 Vault 加密存储，禁止写死在代码或配置中。
- **性能提示**：单次请求最大上下文为 32768 tokens，函数调用本身不额外计费，但调用产生的云资源（如函数计算实例、图像生成）按实际用量计费。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)


