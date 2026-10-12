# 函数调用

函数调用（Function Calling）是百炼平台中实现模型与外部系统协同执行的关键机制，指大语言模型在推理过程中主动识别用户意图、生成结构化工具调用请求（如 API 调用、数据库查询、文件处理等），并由平台或客户端解析、执行、注入结果后继续推理的闭环过程。它不是简单的文本生成，而是模型具备“规划—调用—整合”能力的体现，是构建可操作智能体（Agent）和生产级 AI 应用的核心支撑。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非统一接口能力，而是按服务层级和使用方式差异化实现：

- **基础模型 API 层（OpenAI/DashScope 兼容接口）**：  
  模型本身不原生支持函数调用语义（如 OpenAI `functions` 字段），但可通过 DashScope 原生接口的 `tools` + `tool_choice` 参数显式启用。开发者需预先定义工具 Schema（JSON Schema 格式），模型将输出符合规范的 `tool_calls` 数组；平台不自动执行，需由客户端解析并调用对应服务，再将结果以 `tool_message` 形式回传发起下一轮推理。

- **Managed Agents 托管智能体层**：  
  函数调用被深度封装为「技能（Skill）」能力。开发者注册 HTTP 工具、数据库连接器或内置插件后，在 Agent 配置中声明 `skills` 列表；运行时模型自动决定是否调用、调用哪个 Skill，并由平台沙箱环境安全执行、注入结果、维护多步状态。无需手动解析/拼接消息，真正实现“声明即执行”。

- **[多模态](multi-modal.md)与实时交互场景**：  
  当前文生图、文生视频、实时音视频等专用模型暂不支持函数调用。其扩展能力通过独立参数（如 `prompt_extend`、`turn_detection`、`cache_control`）或配套服务（如 RAG 的 `DashScopeCloudIndex`）实现，不属于函数调用范式。

> ✅ 简单判断：若需模型返回结构化工具调用指令并交由你（或平台）执行 → 用 DashScope `tools`；若希望模型+执行+状态全托管 → 用 Managed Agents + Skill。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 示例 |
|------|----------|------|------|------|
| `tools` | DashScope 原生 API | array[object] | 必填。定义可用工具列表，每个对象含 `type`（固定 `"function"`）、`function.name`、`function.description` 和 `function.parameters`（JSON Schema） | `{"type": "function", "function": {"name": "get_weather", "description": "获取指定城市天气", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}}` |
| `tool_choice` | DashScope 原生 API | string 或 object | 可选。控制调用策略：`"auto"`（模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | `"auto"` |
| `skills` | Managed Agents API | array[string] | 可选。Agent 创建时传入已注册的 Skill ID 列表，平台自动绑定并启用调用能力 | `["http-get-weather", "db-query-sales"]` |
| `tools`（Agent 配置） | Managed Agents（YAML/CLI） | array[object] | 可选。在 Agent 定义中内联声明轻量工具（非 Skill），适用于简单 HTTP 调用，Schema 格式同 DashScope | 同上表示例 |

⚠️ 注意事项：
- `tools` 参数仅 DashScope 原生接口（`/api/v1/services/aigc/text-generation`）和 Managed Agents 支持；[OpenAI 兼容接口](openai-compatible-api.md)不识别该字段。
- 使用 `tools` 时，`model` 必须为支持工具调用的 Qwen 版本（如 `qwen3.8-max`、`qwen3.7-plus`），第三方模型（DeepSeek/Kimi/GLM）暂不支持。
- Managed Agents 中的 Skill 需提前通过 `/v1/skills` API 注册，且凭证需通过 `Vault` 安全注入，不可硬编码。

## 面向开发者，简洁实用

- **快速起步（推荐）**：优先使用 Managed Agents。定义 Skill → 创建 Agent 并绑定 → 发起会话即可获得自动工具调度，省去消息解析、错误重试、上下文拼接等工程负担。  
- **精细控制（进阶）**：选用 DashScope 原生接口 + `tools`。适合需要自定义执行逻辑、集成私有服务、或调试调用链路的场景；务必处理 `tool_calls` 解析、异步执行、结果格式化回传三步。  
- **避坑提示**：  
  - 不要对 OpenAI SDK 的 `chat.completions.create()` 传入 `tools` 参数——它会被忽略；改用 DashScope SDK 或直接调用原生 API。  
  - Managed Agents 的 `skills` 是 ID 列表，不是工具定义；工具定义必须先注册，ID 在注册响应中返回。  
  - 所有工具调用均受平台沙箱限制：禁止本地文件读写、系统命令、未授权网络请求；HTTP 工具仅允许白名单域名。  

函数调用的本质是“让模型学会提问，而非仅回答”。在百炼，它是从 prompt 工程迈向可执行 AI 应用的关键跃迁点——选对层级，事半功倍。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)
- [use cases](../guides/use-cases.md)


