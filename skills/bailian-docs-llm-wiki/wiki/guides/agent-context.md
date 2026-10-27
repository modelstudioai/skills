# agent context

agent context 是百炼平台中用于增强 Agent 推理能力的上下文管理机制，支持将外部知识、历史记忆、结构化数据源等动态注入到 LLM 的 [prompt](prompt.md) 中。它通过统一的抽象层解耦数据接入与模型调用，是构建可靠、可追溯、可调试 Agent 应用的核心基础设施。其设计兼顾灵活性与可控性，适用于 RAG、长期记忆、多源数据融合等典型场景。

## 支持的模型与功能

- **模型兼容性**：当前仅支持 `qwen-max`、`qwen-plus` 及 `qwen-turbo` 系列模型（v2024.06 起），其他模型调用时将忽略 context 字段；[Agent 上下文](../../raw/application-user-guide/agent-context.md) 明确指出该限制。
- **核心功能模块**：
  - **RAG 检索结果注入**：自动拼接知识库召回片段，支持按 relevance score 过滤与截断；
  - **Memory 回溯**：集成 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 模块，可指定 session_id 加载最近 N 轮对话历史；
  - **Connector 数据桥接**：通过预注册的 [Connector](../../raw/application-user-guide/agent-context/overview.md) 实时拉取数据库、API 或文件系统数据；
  - **ParseX 结构化解析**：支持对上传文档（PDF/Word/Excel）执行字段级提取，并作为结构化 context 输入。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context` | object | 否 | 主容器对象，包含 `rag`、`memory`、`connector`、`parsx` 四个子字段（任选其一或组合） |
| `context.rag.knowledge_base_id` | string | 是（若启用 rag） | 知识库 ID，需已在控制台发布 |
| `context.memory.session_id` | string | 是（若启用 memory） | 会话唯一标识，长度 ≤ 64 字符 |
| `context.connector.id` | string | 是（若启用 connector） | Connector 配置 ID，需已授权并启用 |
| `context.parsx.file_id` | string | 是（若启用 parsx） | 文件上传后返回的 `file_id`，有效期 24 小时 |

> **注意**：`context.memory.max_turns` 默认为 5，但 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中旧版示例误写为 `max_history`，应以 SDK 参数签名和 API 文档为准。

## 使用方式

1. 在 `/v1/chat/completions` 请求体中，于 `messages` 外层同级传入 `context` 对象；
2. 每个子模块独立生效，不相互覆盖（例如同时启用 `rag` 和 `memory`，两者内容将合并注入 system [prompt](prompt.md) 前置区）；
3. 上下文内容在 LLM 输入前完成拼接与长度裁剪（按 token 计，上限 8192，超出部分从最早条目开始丢弃）；
4. 开发者可通过 `debug: true` 参数在响应中查看实际注入的 context 片段（含来源标注与 token 统计）。

## 限制和注意事项

- 单次请求最多启用 **3 个 context 子模块**（如 `rag + memory + connector`），超出将返回 `400 Bad Request`；
- `context.parsx` 仅支持已通过 `/v1/files/upload` 上传且状态为 `processed` 的文件，[ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 文档强调此前提；
- 所有 context 数据均在服务端完成注入，**不会透出原始凭证或敏感字段值**（如数据库密码、API Key），但需确保 Connector 配置本身已做最小权限隔离；
- 不支持在流式响应（`stream: true`）中动态更新 context —— context 内容在首次 chunk 发送前即已固化。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


