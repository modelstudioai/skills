# memory library overview

记忆库（Memory Library）是百炼平台提供的长期记忆管理能力，用于在多轮对话中持久化存储和检索用户或应用相关的上下文信息。它支持结构化与非结构化数据的混合存储，并通过向量检索与关键词匹配实现高效召回。该能力面向 LLM 应用开发者，可直接集成至工作流或通过 API 调用。

## 支持的模型/功能

- 当前仅支持接入百炼平台托管的 **Qwen 系列大模型**（如 qwen-max、qwen-plus），不支持第三方模型直连；  
- 提供两类核心功能：**长期记忆存储（write）** 与 **上下文增强式检索（read）**，支持在 `chat` 请求中通过 `memory_id` 自动注入相关记忆片段；  
- 支持按 `user_id`、`session_id`、`tag` 多维元数据过滤，详见 [记忆库](../../raw/application-user-guide/memory-library-overview.md) 文档。

## 关键参数

- `memory_id`: 必填，用于标识独立记忆空间（如 per-user 或 per-bot），需提前创建；  
- `ttl_seconds`: 可选，设置记忆条目过期时间（默认 30 天，最大 365 天）；  
- `embedding_model`: 可选，指定向量化模型（默认为 `text-embedding-v3`），若自定义 embedding 需保持维度一致；  
- `retrieval_top_k`: 检索时返回的最大条目数（默认 5，上限 20），参见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview.md) 中的请求体说明。

## 使用方式

1. **初始化记忆空间**：调用 `POST /v1/memories` 创建 `memory_id`；  
2. **写入记忆**：使用 `POST /v1/memories/{memory_id}/items` 提交文本、元数据及可选 embedding；  
3. **在对话中启用**：在 `chat` 请求的 `parameters.memory` 字段中传入 `{"memory_id": "xxx", "enable": true}`；  
4. 开发者也可直接调用检索接口 `GET /v1/memories/{memory_id}/search` 进行定制化查询，参考 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview.md) 中的插件集成示例。

## 限制和注意事项

- 单个 `memory_id` 下最多存储 **100 万条记忆项**，单条内容长度上限为 **32768 字符**；  
- 检索延迟受数据规模与 `top_k` 影响，生产环境建议 `top_k ≤ 10`；  
- > **注意**：原始文档中提及“支持 Qwen-VL 模型接入记忆库”，但当前 API 实际校验会拒绝非 text-only 模型的 `memory_id` 绑定请求，该描述已过时，请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview.md) 的最新响应码（400 + `invalid_model_for_memory`）为准；  
- 记忆内容不经过模型训练或微调，仅作检索增强用途，敏感数据需自行脱敏。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview.md)


