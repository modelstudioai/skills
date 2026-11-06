# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全场景需求。开发者可根据业务复杂度、可控性要求和运维能力，选择 Managed Agent、Flow Agent 或 Sandbox 模式。所有模式均基于统一的底层运行时与可观测能力，但抽象层级与权限边界存在显著差异。

## 支持的模型/功能

- **Managed Agent**：面向业务人员的托管式 Agent，预置工具链与对话状态管理，无需编码；适用于标准客服、FAQ 等轻量任务。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图的 LLM 应用编排（原称“LLM Application”），支持条件分支、多跳调用、自定义函数节点；是当前推荐的主流开发方式。其能力边界与节点规范在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：提供 Python 运行时沙箱，允许完全自定义逻辑、外部 API 调用及状态持久化，适合需要深度控制推理链路的场景。沙箱的安全策略与资源限制见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

- `agent_type`：必填，取值为 `"managed"` / `"flow"` / `"sandbox"`，决定运行模式与参数校验规则；
- `model_id`：仅 Flow Agent 和 Sandbox 需指定，支持 `qwen-max`、`qwen-plus` 等百炼全量模型；
- `timeout_ms`：默认 30000（30 秒），Sandbox 模式下最大可设为 120000（2 分钟）；
- `enable_tracing`：布尔值，开启后记录完整执行轨迹，用于调试与审计。

## 使用方式

1. 通过 OpenAPI 创建 Agent 实例（`POST /v1/agents`），传入配置 JSON；
2. 对已部署 Agent 发起调用：`POST /v1/agents/{agent_id}/chat`，请求体需包含 `messages` 数组；
3. Flow Agent 支持在控制台拖拽编辑流程图，并一键发布；Sandbox 需上传 `main.py` 及依赖文件（`requirements.txt` 可选）。

## 限制和注意事项

- Managed Agent 不支持自定义模型或超时覆盖，其行为由平台严格管控；
- Flow Agent 的函数节点目前仅支持同步调用，不支持 `async/await`；该限制在 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档中未明确提及，但实际运行会报错；
> **注意**：原始文档中 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 提到“支持 WebSocket 流式响应”，但当前 API 仅对 Flow Agent 开放 `stream=true` 参数，Sandbox 模式暂不支持[流式输出](../concepts/streaming-output.md)——请以 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 的最新接口说明为准；
- 所有 Agent 类型均禁止访问内网地址（如 `10.0.0.0/8`）、本地文件系统（`/tmp` 除外）及 fork 子进程。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


