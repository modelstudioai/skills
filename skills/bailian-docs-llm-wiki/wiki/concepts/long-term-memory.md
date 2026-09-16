# 长期记忆

长期记忆是百炼平台提供的**跨会话、持久化、语义驱动的用户状态管理能力**，用于突破大模型上下文窗口限制，实现用户偏好、历史事件、结构化属性等关键信息的自动提取、向量化存储与精准召回。它不是临时缓存或会话状态，而是独立于推理过程、可编程控制、按用户隔离的生产级记忆服务。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆在百炼生态中存在**两套并行但定位互补的技术路径**，开发者需根据应用架构选择：

- **Memory Library（记忆库）—— 通用 SDK/API 方式**  
  适用于任意自研应用、OpenClaw 框架、或需精细控制写入/检索时机的场景。通过 `AddMemory` / `SearchMemory` 等独立 API 显式操作，支持记忆片段（非结构化事件）、用户画像（结构化 Schema）、双策略（`pro`/`lite`）计费，且与模型调用完全解耦。OpenClaw 用户可通过插件实现零侵入自动捕获（`before_agent_start`/`agent_end` 钩子注入）。

- **Long Term Memory (New) —— 模型原生集成方式**  
  专为 `chat` 接口设计，仅支持 `qwen-max`/`qwen-plus`/`qwen-turbo` 模型。通过请求参数 `long_term_memory: true` 启用，配合 `memory_schema` 定义字段、`retrieve_memory` 触发召回，实现“一次配置、自动生效”的轻量集成。写入与检索由平台在模型调用链路中隐式完成，但**不自动注入 [prompt](../guides/prompt.md)**，需开发者手动拼接 `retrieved_memory` 字段。

- **Application Call（智能体/工作流调用）—— 应用层封装方式**  
  在调用已发布的智能体或工作流时，通过 `memory_id` 参数关联预配置的长期记忆实例，由平台在应用运行时自动启用记忆能力。该方式无需修改业务代码，适合快速接入已有应用，但灵活性低于前两者。

> ✅ 共同原则：所有路径均以 `user_id` 为隔离单位，确保多用户数据严格隔离；均支持元数据（`meta_data`）标注与条件过滤；均依赖统一后端记忆服务，具备一致的语义检索能力。

## 关键参数和配置

| 参数 | 所属路径 | 类型 | 说明 | 是否必填 |
|------|----------|------|------|----------|
| `user_id` | 全路径 | string | 用户唯一标识，决定记忆命名空间。**必须全局一致**（如登录态 ID），否则导致记忆碎片化。 | 是 |
| `plan_version` | Memory Library | string | 检索/写入策略：`pro`（启用 Rerank，高精度低吞吐）、`lite`（禁用 Rerank，低成本高吞吐）。`SearchMemory` 中显式传入优先级最高。 | 否（Search 默认 `pro`；Add 由 `project_id` 决定） |
| `expired_in_days` | Memory Library | integer | 记忆过期天数。**未设置则永不过期**（非默认 180 天）。创建 `MemoryProject` 时指定，影响所有关联记忆。 | 否 |
| `memory_schema` | Long Term Memory (New) | object | JSON Schema 定义需提取的字段（如 `{"city": "string", "budget": "number"}`）。仅用于字段校验与结构化存储，**不参与向量化**。 | 否 |
| `retrieve_memory` | Long Term Memory (New) | object | 控制召回行为：`top_k`（默认 3）、`filter`（KV 条件过滤，如 `{"city": "杭州"}`）。返回结果在响应顶层 `retrieved_memory` 字段。 | 否 |
| `memory_id` | Application Call | string | 已配置的长期记忆实例 ID，在控制台应用设置中绑定。启用后由平台自动接管写入/检索逻辑。 | 否 |

> ⚠️ 注意：  
> - `memory_schema` 字段值长度上限 2048 字符，最多支持 10 个字段；  
> - Memory Library 单 `user_id` 下无硬性条数限制（依赖 `expired_in_days` 或手动清理），而 Long Term Memory (New) 采用 LRU 策略，单用户上限 1000 条；  
> - `plan_version` 在 Memory Library 中**写入与检索完全解耦**：可对 `lite` 写入的数据执行 `pro` 检索，反之亦然。

## 面向开发者，简洁实用

- **选型建议**：  
  - 要最大控制力、多模型兼容、或集成 OpenClaw → 用 **Memory Library**；  
  - 要快速上线、仅用 Qwen 系列 `chat`、且接受结构化 Schema → 用 **Long Term Memory (New)**；  
  - 要复用已有智能体/工作流、最小改造 → 用 **Application Call + `memory_id`**。

- **最佳实践**：  
  - ✅ 写入：`AddMemory` 建议每轮对话结束后异步调用（避免阻塞主流程）；`long_term_memory: true` 写入由平台自动触发，无需额外处理。  
  - ✅ 检索：`SearchMemory` 的 `top_k` 推荐设为 `3–5`；`retrieve_memory.top_k` 默认 `3`，按需调整。  
  - ✅ 过滤：善用 `meta_data`（Memory Library）或 `filter`（New）做业务维度隔离，如 `"category": "reminder"` 或 `"source": "app_a"`。  
  - ❌ 避免：在 `system` 提示词中重复定义 `memory_schema` 字段名（易冲突）；跨 `user_id` 复用记忆；忽略 `user_id` 一致性导致记忆丢失。

- **调试提示**：  
  - 使用 `ListMemory`（Memory Library）或检查 `retrieved_memory` 字段（New）验证写入/召回是否生效；  
  - 高延迟场景下，优先检查配额（Memory Library：`AddMemory ≤120 QPM`；`SearchMemory ≤300 QPM`）；  
  - 记忆未命中？确认 `user_id` 完全一致、`expired_in_days` 未过期、`filter` 条件匹配。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)


