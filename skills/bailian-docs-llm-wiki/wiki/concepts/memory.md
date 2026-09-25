# 记忆

记忆是百炼平台为大模型应用提供的结构化、跨会话长期上下文管理能力，通过自动提取、持久化存储与语义检索用户相关事实信息和结构化画像，使智能体具备持续理解用户意图、偏好与历史行为的能力。它不是简单的对话缓存，而是以 `user_id` 为隔离单元、支持策略化生命周期管理的可编程记忆服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents（托管智能体）**：记忆作为默认启用的上下文增强模块，自动在会话开始前（`autoRecall`）检索匹配该 `user_id` 的事实记忆与用户画像，并注入系统提示词；无需修改 Agent 配置，即可让 `qwen-max` 等模型天然“记得”用户习惯（如“每天9点喝水提醒”或“职业是设计师”）。  
- **Workflow（工作流）与 OpenClaw**：通过「长期记忆插件」集成，开发者可在任意节点调用 `AddMemory` 写入关键事件，或用 `SearchMemory` 检索结果参与条件判断/变量赋值，实现业务逻辑驱动的记忆闭环（例如：订单完成 → 写入“已履约”事实；下次咨询 → 检索并主动告知“上次订单已签收”）。  
- **LLM Application（高代码应用）**：通过 DashScope SDK 或直接调用 RESTful API（`POST /add`, `POST /memory_nodes/search`），在 Python 函数中精细控制记忆写入时机、内容格式与检索策略，适用于需与自有数据库/CRM 对接的定制化场景。  
- **安全体系中**：所有记忆的读写操作均经过内生内容安全引擎检测，自动拦截含敏感信息、违规表述或潜在投毒风险的记忆内容，保障长期记忆库的数据合规性与可信度。  
- **统一抽象层**：无论使用 Agent Harness 零配置、插件拖拽，还是 SDK 编码，底层均基于同一套记忆模型——即 **事实记忆**（动态、时效性事件，如行为/技能/观测）与 **用户画像**（静态、结构化属性，如年龄/职业/偏好），二者可独立使用，亦可协同增强上下文精度。

## 关键参数和配置

| 参数 | 说明 | 建议值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 记忆隔离主键，**必填**。同一 `user_id` 下所有记忆互通；不同 `user_id` 完全隔离。 | 业务侧稳定标识（如用户手机号哈希、OpenID） | 不可为空；不建议使用临时 session_id |
| `plan_version` | 检索策略版本：`pro`（启用 Rerank + `min_score` 过滤，质量高）、`lite`（基础向量检索，延迟低、成本低） | 实时性要求高用 `lite`；精度优先用 `pro`（默认） | `Add` 接口由规则决定；`Search` 接口由请求参数控制 |
| `top_k` | 单次检索最大返回条数 | 3–10（适配 Prompt 上下文容量） | 范围 1–100；过大易超 token 限制 |
| `min_score` | 相似度阈值（0.0–1.0），仅 `plan_version=pro` 时生效 | 0.55–0.65（平衡召回率与准确率） | 低于此值的结果被过滤，不计入 `top_k` |
| `profile_schema` | 用户画像模板 ID，**仅当写入结构化画像时必填** | 通过 `POST /profile_schemas` 创建后获取 | 不传则仅触发事实记忆抽取 |
| `memory_library_id` | 指定自定义记忆库 ID；不传则使用默认库 | 自定义库 ID（如 `mlib-prod-user`） | 默认库不可删除，自定义库可随时清理 |

> ⚠️ 注意：`extract_scene` 参数**仅作用于用户画像模板**，与事实记忆无关；事实记忆质量由 `plan_version` 控制。

## 面向开发者，简洁实用

- ✅ **快速验证三步走**：  
  1. `curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \  
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \  
     -d '{"user_id":"u123","messages":[{"role":"user","content":"我下周要出差去杭州"}]}'`  
  2. 控制台查看是否生成“出差”事实记忆；  
  3. 再次调用 `/search`，传相同 `user_id` 和新 query（如“我最近有什么安排？”），确认结果被注入 Prompt。  

- ✅ **生产就绪要点**：  
  - 限流防护：账号级总限流 3000 QPM，`SearchMemory` ≤ 300 QPM —— 务必实现指数退避重试（HTTP 429）；  
  - 异步画像：`AddMemory` 后立即查 `GetUserProfile` 可能为空，建议等待 3 秒后重试；  
  - 数据隔离：`user_id` 是唯一隔离维度，跨业务共享需应用层聚合，**不支持跨 `user_id` 查询**；  
  - 免费额度：上线前确认免费额度（Add 1500次/3个月，Search 5000次/3个月，存储 10,000 条永久免费）；  
  - 安全合规：所有记忆内容自动过检，但敏感字段（如身份证号）仍需业务侧脱敏后再写入。  

- ❌ **避免踩坑**：  
  - 不要将 `user_id` 设为随机字符串（导致记忆无法复用）；  
  - 不要在 `SearchMemory` 中传 `messages` 为空数组（将返回空结果）；  
  - 不要依赖默认库的“自动清理”——记忆无自动过期机制，需按业务规则显式管理生命周期（如调用 `/memory_nodes/{id}` 删除）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [security guide](../guides/security-guide.md)
- [llm application](../guides/llm-application.md)


