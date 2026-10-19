# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同机制，允许大模型在推理过程中主动识别用户意图、生成符合预定义 Schema 的函数调用请求（而非仅输出自然语言），由平台或客户端执行对应工具后将结果注入上下文，驱动多步、确定性、可验证的智能体行为。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力在百炼平台中并非全局统一启用，而是按**服务层级与模型/应用类型**差异化支持：

- **基础模型 API（`/v1/chat/completions`）**：部分 Qwen 系列模型（如 `qwen-max`、`qwen3.8-max`）原生支持函数调用。需在请求中显式传入 `functions`（工具列表）和 `function_call`（调用策略），模型将返回 `{"role": "function", "name": "...", "arguments": "..."}` 类型的消息。适用于需要轻量级工具集成、自主决策链路较短的场景。

- **智能体应用（Agent Application）**：新版智能体（Agent 2.0）和 Managed Agents 均深度集成函数调用能力，但实现方式不同：
  - *Agent 应用*：通过 `biz_params.tools` 或控制台配置的插件自动注册为可调用函数；模型无需显式声明 `functions`，平台在运行时自动注入工具 Schema 并解析调用。
  - *Managed Agents*：工具（如 `bash`、`web_search`、`read`）作为沙箱内置能力被严格管控；函数调用由 Agent 运行时自动触发、沙箱执行、结果回填，开发者只需配置 `tools` 列表及权限策略（如 `always_allow`），无需手动处理 JSON Schema 或 arguments 解析。

- **工作流（Workflow）**：不直接暴露函数调用接口，但可通过「工具节点」封装函数逻辑，在流程图中以可视化方式编排调用顺序与条件分支，本质是函数调用的低代码抽象。

> ⚠️ 注意：函数调用能力**依赖模型本身支持**，并非所有模型均可用。调用前请查阅对应模型文档确认 `function_calling: true` 标识，并注意地域限制（如北京地域优先保障完整能力）。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必需 |
|------|------|------|------|----------|
| `functions` | 请求 body（模型 API） | array of object | 工具定义数组，每个对象含 `name`、`description`、`parameters`（JSON Schema）字段。用于告知模型可用工具及其输入约束。 | 否（但启用函数调用必须提供） |
| `function_call` | 请求 body（模型 API） | string / object | 控制调用策略：<br>- `"auto"`（默认）：模型自主决定是否调用；<br>- `"none"`：禁用调用；<br>- `{"name": "xxx"}`：强制调用指定函数。 | 否（默认 auto） |
| `tools` | Agent 配置 / Session 创建参数 | array of object | Managed Agents 和新版智能体中声明启用的工具列表，格式为 `[{ "type": "builtin", "name": "web_search" }]` 或 `[{ "type": "mcp", "name": "xxx" }]`。 | 是（若需工具能力） |
| `tool_choice` | Agent 配置（高级） | string / object | 类似 `function_call`，用于 Agent 场景下约束工具选择策略（如 `"required"` 强制调用）。 | 否 |
| `permission_policy.type` | `tools[].configs[]`（Managed Agents） | string | 工具执行审批策略：`"always_allow"`（自动执行）、`"always_ask"`（需人工确认）。影响函数调用的实际落地。 | 否（默认 `always_allow`） |

- 所有函数调用请求均需确保 `messages` 中包含足够上下文（如用户问题、历史对话），模型才能准确生成合法 `arguments`。
- `arguments` 字段为 JSON 字符串，**必须严格符合 `parameters` 定义的 Schema**，否则将导致解析失败或工具执行异常。

## 面向开发者，简洁实用

- ✅ **快速验证**：从最小可行示例开始——使用 `qwen-max` 模型 + 一个简单工具（如 `get_current_weather`），发送含 `functions` 的请求，观察响应中是否出现 `role: "function"` 消息。
- ✅ **调试技巧**：若模型未触发调用，检查 `functions` 描述是否清晰、`parameters` Schema 是否过于复杂、用户 query 是否明确暗示工具需求；开启 `temperature=0` 可提升确定性。
- ✅ **生产建议**：避免在 `functions` 中定义过多工具（建议 ≤5 个核心工具），优先使用 `function_call: "auto"` 让模型自主决策；对关键业务工具，务必配置 `permission_policy.type: "always_allow"` 并做好错误重试。
- ❌ **不要** 将函数调用与普通文本生成混用——一旦启用，模型输出即进入“工具协议模式”，后续消息需按 `role: function` → `role: assistant` 流程处理，不可跳过解析步骤直接渲染。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [agent development](../guides/agent-development.md)


