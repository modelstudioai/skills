# 函数调用

函数调用是百炼平台中模型或智能体主动触发外部能力（如插件、内置工具、MCP服务）执行具体任务的核心机制，本质是将自然语言指令解析为结构化工具请求，并同步/异步完成执行与结果回传。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用并非独立功能，而是贯穿于多个运行时环境的底层交互范式，其触发方式、控制粒度和上下文依赖因场景而异：

- **插件（Plug-in）场景**：在智能体应用或工作流中，模型根据用户意图自动识别并调用已绑定的插件（如 `calculator`、`quark_search`）。调用由大模型生成符合 OpenAPI Schema 的参数，经平台校验后转发至插件服务端；支持“大模型识别”（自动抽取）和“业务透传”（通过 `biz_params.user_defined_params` 显式注入）两种参数来源。
  
- **智能体应用（LLM Application / Agent 1.0 & 2.0）**：函数调用表现为插件节点的执行。工作流画布中，插件作为独立节点被编排；Agent 应用中，调用由模型自主决策发起，平台负责参数构造、鉴权透传与错误重试。注意：Agent 2.0 默认启用记忆，历史调用结果可参与后续推理。

- **托管智能体（Managed Agents）**：函数调用更底层、更可控——不仅支持插件，还直接暴露沙箱级内置工具（如 `bash`、`read`、`web_fetch`）及 MCP 协议服务。开发者需在 `tools` 配置中**显式启用每个工具**（`"enabled": true`），否则模型无法发现；调用过程在隔离沙箱中执行，支持多步交互、文件读写与状态持久化。

- **API 调用层（Application Call / Flow Agent API）**：函数调用能力通过 `biz_params` 向下透传。例如，在 `/v1/apps/{app_id}/completion` 接口中，通过 `biz_params.user_defined_params` 将参数精准注入指定插件；在 Managed Agents 会话中，则通过 `tools` 配置与 `resources` 挂载共同定义可调用函数集。

> ✅ 关键区别：插件调用强调“模型驱动+标准化接入”，适用于快速扩展能力；托管智能体工具调用强调“开发者强控+沙箱执行”，适用于复杂、有状态、需调试的任务。

## 关键参数和配置

函数调用的可靠性高度依赖以下参数的正确定义与传递：

- **工具标识**  
  - `tool_id`（插件）：唯一字符串，如 `"calculator"`，必须与控制台发布的插件工具 ID 完全一致；  
  - `name`（托管智能体内置工具）：如 `"bash"`，需在 `tools` 数组中声明并设 `enabled: true`。

- **输入参数**  
  - 类型严格：支持 `string`、`number`、`boolean`、`object`；`object` 类型子字段不可为空；  
  - 透传路径：  
    - 插件场景 → `biz_params.user_defined_params.{tool_id}`；  
    - 托管智能体场景 → 由模型生成或通过 `tools` 配置预设 `default_input`；  
  - 示例值建议：在插件配置中设置 `Value` 示例（如 `{"query": "杭州天气"}`），显著提升参数构造准确率。

- **鉴权与网络**  
  - 自定义插件需配置鉴权方式（`Header` 或 `Query`），`Type` 可选 `bearer`/`basic`/`appcode`；  
  - 托管智能体环境需提前配置 `environment_id` 并确保网络策略（如 `unrestricted`）允许工具访问目标服务。

- **调用控制**  
  - `stream`：启用流式响应（SSE），便于实时展示调用过程；  
  - `debug: {}`：启用后返回完整工具调用日志、参数快照与执行耗时，强烈推荐调试阶段开启；  
  - `flow_stream_mode`（工作流专用）：设为 `"message_format_plus"` 可清晰分离工具调用请求与结果事件。

## 面向开发者，简洁实用

- ✅ **必做三件事**：  
  1. 确认模型兼容性——`qwen-plus`/`qwen-max` 支持插件；`qwen3.8-max`/`deepseek-v4.1-flash` 等支持托管智能体工具；  
  2. 显式启用工具——尤其在 Managed Agents 中，`default_config.enabled: true` 不生效，必须逐个设 `enabled: true`；  
  3. 用 `debug` 模式验证首次调用——检查 `user_defined_params` 是否到达、参数是否被截断、鉴权 Header 是否正确注入。

- ⚠️ **避坑提醒**：  
  - GET 类插件不支持 `object` 输入参数；  
  - `code_interpreter` 沙箱无外网访问能力，勿尝试 `requests.get("https://...")`；  
  - 删除插件或工具将导致所有关联应用失效，且操作不可逆；  
  - 工作流应用仅支持华北2（北京）地域，且不支持文生图类大模型。

- 🚀 **进阶提示**：  
  - 多智能体协作中，函数调用可跨 agent 分发（如 coordinator 调用 `web_search`，worker 调用 `bash` 处理结果）；  
  - 结合[长期记忆](long-term-memory.md)（`memory_id`），让工具调用结果自动沉淀为后续对话的知识依据；  
  - 使用 `biz_params` 实现用户级鉴权透传（如将用户 OAuth [Token](token.md) 注入插件请求头），实现租户隔离。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [agent development](../guides/agent-development.md)
- [flow agent api](../api/flow-agent-api.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


