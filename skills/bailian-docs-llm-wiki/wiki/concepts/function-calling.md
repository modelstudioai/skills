# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由系统或开发者后端执行外部操作的核心能力。它使大模型不仅能生成文本，还能安全、可控地与数据库、API、插件等外部系统交互，是构建 Agent、自动化工作流和增强型应用的关键机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **Sandbox 环境**：在沙箱中调试时，函数调用能力默认启用（需模型支持，如 `qwen-max`、`qwen-plus`）。模型会根据 system [prompt](../guides/prompt.md) 和对话上下文，输出符合 OpenAI-style `function_call` 格式的 JSON 结构；开发者可通过沙箱的 `chat/completions` 接口观察完整调用链路（含工具选择、参数填充、结果注入），用于验证工具 Schema 设计与 [prompt](../guides/prompt.md) 工程效果。

- **Application Call（应用调用）**：当应用配置了工具（内置插件或自定义函数），平台会在推理过程中自动启用函数调用流程。模型返回 `tool_calls` 后，百炼服务层自动执行对应插件（如夸克搜索、代码解释器）或转发至开发者注册的 Webhook；执行结果将作为 `tool_message` 注入下一轮上下文，实现多步推理闭环。该过程对调用方透明，无需手动解析/触发。

- **Application Monitoring（应用观测）**：函数调用被作为独立 Span 类型埋点上报，可观测字段包括 `tool_name`、`tool_input`（脱敏）、`execution_duration_ms`、`status`（success/failed/timeouted）及错误码（如 `TOOL_EXECUTION_TIMEOUT`）。开发者可通过 `trace_id` 下钻分析某次调用中函数调用是否被触发、耗时是否异常、失败是否源于参数校验或网络超时。

- **Application Support（应用支持）**：平台提供两类函数调用支持：  
  - **内置插件**：开箱即用（如计算器、图片生成），无需注册，仅需在应用配置中启用；  
  - **自定义函数**：需按 OpenAPI 3.0 Schema 注册函数元信息（名称、描述、参数类型与约束），百炼模型据此理解语义并生成合法参数。注意：调用时仅 `Authorization` Header 可透传，其余自定义 Header 将被丢弃。

## 关键参数和配置

- **工具注册 Schema**（自定义函数必需）：  
  - `name`（string，必填）：函数唯一标识，需符合 Python 变量命名规范（字母/数字/下划线，不以数字开头）；  
  - `description`（string，必填）：简洁说明函数用途（影响模型调用准确性）；  
  - `parameters`（object，必填）：JSON Schema 定义，建议显式声明 `type`、`description` 及 `required` 字段；避免使用过于宽泛的 `anyOf` 或嵌套过深结构。

- **调用控制参数**（通过 `parameters` 透传至应用或沙箱）：  
  - `enable_function_calling`: bool，默认 `true`；设为 `false` 可临时禁用所有工具调用（模型将纯文本响应）；  
  - `max_function_calls`: int，默认 `3`；限制单次推理中最多触发的函数调用次数，防止无限循环；  
  - `function_call_timeout_ms`: int，默认 `10000`（10 秒）；单个函数执行超时阈值，超时后标记为失败并注入错误消息。

- **监控相关配置**（影响可观测性）：  
  - `enable_monitoring`（全局开关）：必须开启才能采集函数调用 Span；  
  - `sampling_rate`：建议生产环境设为 `0.1–0.3`，避免高并发下埋点开销过大。

## 面向开发者，简洁实用

- ✅ **调试建议**：在 Sandbox 中先用简单 [prompt](../guides/prompt.md)（如“查今天北京天气”）验证函数是否被触发；检查返回的 `tool_calls` 字段是否存在且 `name` 匹配注册名。  
- ✅ **Schema 最佳实践**：参数名用小写+下划线（如 `city_name`），避免驼峰；必填参数明确声明 `required: ["city_name"]`；字符串参数加 `minLength`/`maxLength` 约束。  
- ⚠️ **注意边界**：函数调用不支持跨 [sandbox](../guides/sandbox.md) 实例共享状态；自定义函数 Webhook 必须在 10 秒内返回 HTTP 2xx 响应，否则视为超时；返回体需为 JSON，且顶层字段 `content` 将作为模型下一轮输入。  
- 🚀 **快速集成**：使用百炼 SDK 的 `App` 类时，直接传入 `tools=[...]` 即可自动注册并启用函数调用，无需手动处理 `tool_calls` 解析与回调。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [application call](../api/application-call.md)
- [application monitoring](../guides/application-monitoring.md)
- [application support](../guides/application-support.md)


