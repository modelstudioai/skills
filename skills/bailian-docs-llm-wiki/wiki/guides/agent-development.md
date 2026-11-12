# agent development

Agent 开发是百炼平台提供的核心能力之一，支持开发者快速构建具备多步推理、工具调用和状态管理的智能体应用。平台提供多种开发范式，覆盖从低代码配置到全代码自定义的完整链路。所有 Agent 类型均基于统一的运行时框架，但模型支持、参数控制和部署方式存在差异。

## 支持的模型/功能

- **Managed Agent**：面向业务场景封装的托管式 Agent，内置日程、客服、数据查询等模板，支持通过 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档了解预置能力与接入方式。  
- **Flow Agent**：基于可视化流程图构建的 LLM 应用（原称 LLM Application），支持节点编排、条件分支与自定义函数，详细说明见 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md)。  
- **Sandbox**：提供隔离 Python 运行环境，允许执行任意代码逻辑并调用外部 API，适用于需要强计算或私有逻辑的场景，参见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。  

> **注意**：文档中提及的“应用广场”为历史遗留入口，当前已下线；新应用应通过控制台「Agent 应用」列表直接创建或导入，[应用广场](../../raw/application-user-guide/agent-development/application-gallery.md) 文档内容已过时，不建议参考。

## 关键参数

- `model_id`：必须指定，仅支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分 `qwen-vl` 等百炼专属模型；通用开源模型（如 Llama3）暂不支持 Agent 模式。  
- `enable_thinking`：布尔值，启用后开启多步推理链（默认 `true`），影响 token 消耗与响应延迟。  
- `max_iterations`：最大推理步数，默认 15，超过将强制终止并返回 `STOP` 状态。  
- `tools`：工具列表需显式声明，格式为 `{ "name": "...", "description": "...", "parameters": {...} }`；工具函数签名必须与注册时一致。

## 使用方式

1. 在控制台创建 Agent 应用，选择类型（Managed / Flow / Sandbox）；  
2. 配置基础参数（模型、超时、调试开关等）；  
3. 若为 Flow Agent，通过画布拖拽节点并连接逻辑流；若为 Sandbox，上传 `main.py` 入口文件；  
4. 调用时通过 `/v1/agents/{agent_id}/chat` 接口提交 `messages` 数组，支持流式响应（`stream=true`）；  
5. 所有 Agent 均支持异步任务模式（`mode=async`），适用于长周期任务，结果通过回调 URL 或轮询获取。

## 限制和注意事项

- 单次请求最大上下文长度为 32k tokens（含工具描述与历史消息），超出将触发截断警告；  
- Sandbox 模式下禁止访问内网地址、执行系统命令（`os.system`、`subprocess` 等）及读写本地文件系统；  
- Managed Agent 不支持自定义工具注入，仅能启用/禁用预置工具集；  
- Flow Agent 的节点间数据传递上限为 1MB，超限将导致流程中断。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


