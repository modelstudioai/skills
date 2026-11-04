# agent api start using

Agent API 是百炼平台提供的面向智能体（Agent）应用开发的核心接口集合，支持构建具备规划、工具调用、多步推理与外部系统集成能力的自主智能体。开发者可通过统一 HTTP 接口或官方 SDK 快速接入 Managed Agents、Flow Agents 等多种 Agent 类型。本文档聚焦快速上手路径，涵盖模型支持、关键参数、调用方式及约束条件。

## 支持的模型/功能

Agent API 本身不直接绑定特定大模型，而是通过底层 `model_id` 参数指定所用推理模型（如 `qwen-max`、`qwen-plus`），实际能力取决于所选模型是否支持 tool calling、function calling 或 structured output。当前完整支持的 Agent 类型包括：
- **Managed Agents**：托管式智能体，自动处理记忆、工具调度与状态管理，详见 [Managed Agents API](raw/application-api-reference/managed-agents-api.md)；
- **Flow Agents**：基于可视化编排流程的智能体，支持节点化逻辑控制，详见 [Flow Agent API](raw/application-api-reference/flow-agent-api.md)；
- **Sandbox API** 和 **RAG API**：分别提供安全沙箱执行环境与[检索增强生成](../concepts/rag.md)能力，是构建可靠 Agent 的关键扩展组件，详见 [Sandbox API](raw/application-api-reference/sandbox-api.md) 和 [RAG API](raw/application-api-reference/rag-api.md)。

> **注意**：文档中提及的 “Assistant API（下线中）” 已于 2024 年 9 月起停止新应用接入，存量调用将于 2025 年 3 月全面终止，迁移请参考 [Agent API 指南](../../raw/application-api-reference/agent-api-start-using/agent-api-guide.md)。

## 关键参数

发起 Agent 调用时，必需参数包括：
- `agent_id`：Agent 实例唯一标识（由控制台创建后分配）；
- `model_id`：指定底层推理模型 ID，需与 Agent 类型兼容（例如 Flow Agent 不支持 `qwen-turbo`）；
- `input`：用户输入内容，为字符串或结构化对象（如 `{ "text": "...", "files": [...] }`）；
- `stream`：布尔值，控制是否启用流式响应（默认 `false`）；
- `enable_thinking`：仅 Managed Agents 支持，启用后返回中间思考链（Thinking Trace），详见 [Managed Agents API 概览](../../raw/application-api-reference/managed-agents-api.md)。

## 使用方式

1. **认证准备**：确保已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，Managed Agents 的密钥作用域需在业务空间内显式授权；
2. **选择 SDK 或 HTTP 调用**：推荐使用 Python SDK（v1.22.0+）或 Java SDK（v1.18.0+），安装方式与版本要求见 [Managed Agents API 概览](https://help.aliyun.com/zh/model-studio/managed-agents-api-overview#h-sdk)；
3. **发起请求**：以 Managed Agent 为例，Python SDK 示例：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client("<your-access-key-id>", "<your-access-key-secret>", "cn-beijing")
   response = client.run_agent(
       agent_id="agt-xxx",
       model_id="qwen-max",
       input={"text": "今天北京天气如何？"},
       stream=False
   )
   ```

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 32768 字符；若含文件，总上传体积不超过 50 MB；
- Managed Agents 默认开启[长期记忆](../concepts/long-term-memory.md)（Long-term Memory），其存储策略与生命周期受 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 文档约束；
- Flow Agent 的节点超时时间为 30 秒/节点，整条流程总耗时不可超过 180 秒；
- 所有 Agent 类型均**不支持跨地域调用**：`agent_id` 与 API 请求 endpoint 必须位于同一地域（如 `cn-beijing`）；
- 安全敏感场景需启用 [Security API](../../raw/application-api-reference/security-api-guide.md) 进行内容过滤与风险拦截。

## 来源文档

- [Agent API](../../raw/application-api-reference/agent-api-start-using/agent-api-guide.md)


