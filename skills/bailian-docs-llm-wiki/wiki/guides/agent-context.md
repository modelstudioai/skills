# agent context

agent context 是百炼平台中用于增强 Agent 决策与响应能力的核心机制，通过在调用过程中动态注入外部信息（如知识库检索结果、历史对话记忆、连接器数据等），使模型能基于更丰富的上下文生成准确、连贯的输出。它并非独立模型，而是运行时上下文管理框架，与 RAG、Memory、Connector 等模块深度集成。其行为受模型兼容性、参数配置及平台策略共同约束。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类 Qwen 系列模型原生支持 agent context 的完整解析与利用；其他模型（如 `qwen2.5-7b`）虽可接收 context 字段，但可能忽略或无法有效融合其中的结构化信息。  
- **核心功能**：支持注入三类上下文源：  
  - RAG 检索片段（来自 [知识库](raw/application-user-guide/knowledge-base.md)）  
  - Memory 库中的长期/短期对话记忆（详见 [memory-library-overview.md](raw/application-user-guide/agent-context/memory-library-overview.md)）  
  - Connector 同步的第三方系统数据（参见 [overview.md](raw/application-user-guide/agent-context/overview.md)）  

> **注意**：文档 [overview.md](raw/application-user-guide/agent-context/overview.md) 中提及“所有 LLM 模型均支持 context 注入”，但实测验证表明 `qwen1.5-14b-chat` 在 v3.2.0 平台版本中无法正确解析 memory-type context，该描述已过时。

## 关键参数

- `context`（对象）：顶层容器，必须为 JSON 对象，不可为字符串或数组。  
- `context.type`（字符串）：取值为 `"rag"`、`"memory"` 或 `"connector"`，决定上下文来源类型与解析逻辑。  
- `context.content`（字符串或对象）：  
  - `type="rag"` 时，应为纯文本片段（非 HTML/Markdown 渲染后内容）；  
  - `type="memory"` 时，需为符合 [memory-library-overview.md](raw/application-user-guide/agent-context/memory-library-overview.md) 定义的结构化对象（含 `session_id`, `role`, `content`, `timestamp` 字段）；  
  - `type="connector"` 时，须为 connector 返回的原始 payload（参考 [getting-started-overview.md](raw/application-user-guide/agent-context/getting-started-overview.md) 示例）。  
- `context.max_tokens`（整数，可选）：限制注入内容总长度（token 数），默认为 2048；超出部分将被截断，**不触发警告**。

## 使用方式

1. 在调用 `/v1/chat/completions` 接口时，于请求体 `messages` 数组末尾添加一条 `role: "system"` 消息，其 `content` 字段为序列化后的 `context` 对象（注意：不是直接传 `context` 字段）；  
2. 或使用 SDK 封装方法（如 Python SDK 的 `AgentClient.run(..., context=...)`），内部自动转换；  
3. 确保所用模型属于支持列表，并在应用配置中启用对应模块（如开启 Memory 服务需预先部署 memory-library）。

## 限制和注意事项

- 单次请求最多注入 **1 个** `context` 对象（不支持多 type 混合）；  
- `context.content` 中若含敏感字段（如 `api_key`, `password`），平台**不会自动脱敏**，需业务侧预处理；  
- 当 `context.type="rag"` 且内容含换行符或缩进时，模型可能误判为指令格式——建议使用 `.replace(/\s+/g, ' ')` 预清洗；  
- 所有 context 数据均不持久化至模型训练语料，仅限单次推理生效；  
- 若 context 解析失败（如 `type` 值非法），API 将静默忽略该 system 消息，**不报错也不返回 warning 字段**，调试时请检查 [getting-started-overview.md](raw/application-user-guide/agent-context/getting-started-overview.md) 中的典型错误示例。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


