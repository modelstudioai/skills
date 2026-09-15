# 长期记忆

长期记忆是百炼平台提供的**跨请求、跨会话的结构化信息持久化与语义检索能力**，用于在多轮对话或长时间运行的 AI 应用中可靠地存储、索引和召回用户偏好、对话上下文、业务实体等关键状态信息。它不依赖模型自身上下文窗口，而是通过独立的向量+元数据混合存储服务实现低延迟、高相关性的长期状态管理。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆并非单一功能模块，而是以两种互补形态深度集成于平台核心能力中：

- **记忆库（Memory Library）**：面向通用、自主可控的记忆管理需求。适用于客服助手、个性化推荐、知识增强型 Agent 等需灵活写入与复杂过滤的场景。开发者直接调用 `upsert`/`search` API，完全掌控数据结构、集合划分与检索逻辑；支持按 `user_id`、`session_id`、`tag` 等任意业务字段进行元数据过滤，适合构建多租户、多维度记忆体系。

- **长期记忆（新）（Long Term Memory New）**：面向托管式、轻量级状态延续需求。深度耦合于 `qwen-max`/`qwen-plus`/`qwen-turbo` 模型调用链路，通过 `memory_id` 自动隔离用户级状态空间。适用于 Managed Agents、LLM Application 中的会话级上下文延续（如多步骤任务跟踪、用户意图沉淀），无需显式构造向量查询，仅需传入自然语言 `query` 即可触发语义召回。其设计强调开箱即用与模型协同，但功能粒度较粗（不支持单条更新/删除，仅支持整 `memory_id` 清空）。

> ⚠️ 注意：二者**互不兼容**——Memory Library 的数据无法被 Long Term Memory New 的 `retrieve_memory` 接口访问，反之亦然。选择依据取决于你的架构模式：若需精细控制、多模型复用或自定义索引逻辑，请用 Memory Library；若构建基于 Qwen 系列的托管 Agent 或追求极简接入，请用 Long Term Memory New。

## 关键参数和配置

| 场景 | 参数名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| **Memory Library** | `collection_name` | string | 是 | 记忆集合名称，全局唯一，命名须符合 `[a-z0-9_-]{3,64}` 正则；**缺失将导致 400 错误** |
| | `content` | string | 是 | 待存文本（≤ 8192 字符） |
| | `metadata` | object | 否 | 扁平键值对（≤10 个 key，单 value ≤1024 字符），用于后续 `filter` |
| | `filter` | object | 否 | 检索时元数据条件，支持 `==`、`!=`、`in` 运算符 |
| | `top_k` | int | 否 | 默认 5，范围 1–50；返回最相关条目数 |
| **Long Term Memory New** | `memory_id` | string | 是 | 用户级唯一标识（1–64 字符，仅限字母/数字/`_`/`-`），首次 `write_memory` 时自动初始化空间 |
| | `query` | string | 是（`retrieve_memory` 时） | 自然语言查询句（≤512 字符），系统自动嵌入，**不可替换 embedding 模型** |
| | `top_k` | int | 否 | 默认 **3**（非文档旧示例中的 5），范围 1–10 |
| | `filter` | object | 否 | 支持 `eq`/`in`/`contains` 操作符；字段名**不可以下划线 `_` 开头**（系统保留） |

> 🔑 共同约束：  
> - 所有 `content` 最大长度均为 **8192 字符**；  
> - `metadata` 中**禁止存放明文敏感信息**（如手机号、身份证号），平台不提供字段级脱敏；  
> - 向量索引更新存在约 **30 秒延迟**，高实时性场景需设计重试逻辑；  
> - 无自动 TTL 过期机制（当前生产环境 v20240701 起仍为永久存储，需显式 `clear_memory` 或批量清理）。

## 面向开发者，简洁实用

- ✅ **快速上手**：优先使用 SDK（如 Python `baiyin.MemoryClient`）而非裸 API，自动处理鉴权、重试与序列化。  
- ✅ **写入优化**：批量 upsert（≤100 条/次）；避免高频小写入（易触发限流）。  
- ✅ **检索提效**：善用 `filter` 缩小搜索空间（如 `{"user_id": "u123", "category": "order"}`），比纯向量检索更快更准。  
- ⚠️ **避坑指南**：  
> - 不要混淆 `collection_name`（Memory Library）与 `memory_id`（Long Term Memory New）——它们属于不同服务，无映射关系；  
> - 不要在 `metadata` 中存敏感字段；如需关联用户身份，用脱敏 ID（如 `user_id_hash`）代替原始 ID；  
> - `top_k=10` 并不总比 `top_k=3` 更好，过多低分结果会增加 token 开销与后处理成本，建议先用默认值 3/5 基准测试；  
> - 长期记忆 ≠ 会话历史缓存。Managed Agents 的“7 天会话保留”是平台自动维护的对话快照，与长期记忆的结构化存储无关，二者应分层使用：短期上下文走会话管理，长期状态走记忆库或 LTM New。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [sandbox](../guides/sandbox.md)


