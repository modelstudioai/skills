# memory library overview

记忆库（Memory Library）是百炼平台提供的[长期记忆](../concepts/long-term-memory.md)管理能力，用于在多轮对话中持久化、检索和复用用户或应用相关的结构化信息。它支持向量存储与元数据过滤结合的混合检索，适用于客服助手、个性化推荐等需上下文延续的场景。该能力通过统一 API 封装底层向量数据库与索引逻辑，开发者无需直接管理存储细节。

## 支持的模型/功能

- 支持所有接入百炼平台的 LLM 模型（包括 Qwen 系列、GLM 系列及第三方模型），但[向量嵌入](../concepts/embedding.md)默认使用 `text-embedding-v1`，不可自定义嵌入模型；如需更换嵌入模型，需联系技术支持——此限制在 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/modelstudio-memory-for-openclaw.md) 中有明确说明。
- 提供两类核心功能：**[长期记忆](../concepts/long-term-memory.md)写入（upsert）** 与 **语义检索（search）**，支持按 `user_id`、`session_id`、`tag` 等字段进行元数据过滤。
- 检索结果默认返回 top-k（k ≤ 50）最相关条目，并附带相似度分数；高级排序（如时间衰减加权）需在应用层实现。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `collection_name` | string | 是 | 记忆集合名称，需全局唯一，命名须符合 `[a-z0-9_-]{3,64}` 正则规则 |
| `content` | string | 是 | 待存入的文本内容（长度 ≤ 8192 字符） |
| `metadata` | object | 否 | 键值对形式的结构化标签，总键数 ≤ 10，单值长度 ≤ 1024 字符 |
| `filter` | object | 否 | 检索时的元数据匹配条件，支持 `==`、`!=`、`in` 运算符（详见 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)） |

> **注意**：`collection_name` 在 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 文档中被错误描述为“可选”，实际调用 API 时缺失将导致 400 错误；请以 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 的定义为准。

## 使用方式

1. **初始化**：调用 `POST /v1/memory/collections/{collection_name}/upsert` 写入记忆条目；
2. **检索**：调用 `POST /v1/memory/collections/{collection_name}/search`，传入 `query` 和可选 `filter`；
3. **批量操作**：单次 upsert 最多支持 100 条记录；search 不支持跨 collection 联合查询。

SDK 示例（Python）：
```python
from baiyin import MemoryClient
client = MemoryClient(api_key="YOUR_KEY")
client.upsert("my_collection", content="用户偏好咖啡因", metadata={"user_id": "u123", "category": "diet"})
results = client.search("my_collection", query="用户喜欢喝什么", filter={"user_id": "u123"})
```

## 限制和注意事项

- 单个 collection 最大容量为 100 万条记录，超出后写入失败（无自动清理机制）；
- 元数据字段不支持嵌套对象或数组，仅接受扁平 key-value；
- 向量索引更新存在约 30 秒延迟，实时性敏感场景需预留重试逻辑；
- 所有数据默认加密落盘，但 `metadata` 中**禁止存放明文敏感信息**（如身份证号、手机号），该要求在 [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md) 中未强调，需开发者自行遵循数据安全规范。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview.md)


