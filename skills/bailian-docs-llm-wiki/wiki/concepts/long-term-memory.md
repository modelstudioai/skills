# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、跨会话持久化记忆管理能力，用于突破大模型上下文窗口限制，实现用户状态、行为事实与静态画像的自动提取、语义检索与上下文注入。它以 `user_id` 为隔离单元，通过标准化 REST API 提供写入、检索、更新、删除等全生命周期操作，是构建个性化、连贯、有“记忆”的智能体的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）场景**：  
  在 Agent Harness 或 Managed Agents 中，长期记忆作为默认启用的上下文增强模块。Agent 每次响应后，系统自动调用 `AddMemory` 从对话流中提取事实（如“帮我订下周三的会议室”）或填充用户画像（如“32岁，前端工程师，喜欢 hiking”）；后续轮次中，`SearchMemory` 会基于当前 query 语义召回相关记忆，并注入 [prompt](../guides/prompt.md)，使 Agent “记得”历史承诺、偏好与上下文。

- **工作流（Workflow）场景**：  
  可在任意节点（如 AI 节点或自定义函数节点）中显式调用记忆库 API（如 `SearchMemory`），将检索结果作为变量输入下游节点。例如：条件判断节点先查用户历史投诉次数，再决定是否升级服务；RAG 节点可融合知识库 + 记忆库双源上下文，提升回答准确性。

- **高代码应用（Rich Code Application）场景**：  
  开发者可在 `main.py` 中直接集成 `agentscope-runtime` SDK 或调用原生 REST API，实现细粒度控制。例如：在 `/process` 接口内，先 `SearchMemory` 获取用户订阅偏好，再调用外部 API 推送定制化新闻；或在工具执行后，用 `AddMemoryAsync` 异步记录操作结果，避免阻塞主流程。

- **安全与治理场景**：  
  所有记忆读写操作均受百炼内生安全能力保护：内容在写入前经默认防护扫描（防敏感信息泄露、恶意指令注入）；高级防护可对记忆检索请求进行风险监测（如异常高频查询某用户画像），审计日志完整记录 `user_id`、操作类型、时间戳与 API 调用链路，满足合规追溯要求。

## 关键参数和配置

| 参数 | 必填 | 说明 | 建议值/注意事项 |
|------|------|------|----------------|
| `user_id` | ✅ | 用户唯一标识，所有记忆按此隔离。不同 `user_id` 数据完全不可见。 | 使用业务侧稳定 ID（如 `uid_123456`），避免使用临时 session_id。 |
| `messages` | ✅（`AddMemory`/`SearchMemory`） | 对话历史数组，格式为 `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`。系统据此自动提取事实或检索语义。 | `SearchMemory` 中建议仅传当前 query（单条 user message），避免噪声干扰召回质量。 |
| `plan_version` | ⚠️（推荐显式指定） | `"pro"`（高精度，支持 `min_score` 和 Rerank）或 `"lite"`（轻量级，低成本）。`SearchMemory` 默认 `"pro"`；`AddMemory` 默认由规则配置决定。 | 生产环境关键任务（如医疗咨询、金融推荐）务必设为 `"pro"`；内部测试可用 `"lite"` 降本。 |
| `top_k` | ❌（可选） | `SearchMemory` 最大召回条数，默认 `10`，范围 `1–100`。 | 初始调试建议 `5–10`；若需多角度参考（如生成报告），可设 `20–30`，但需注意 token 开销。 |
| `min_score` | ⚠️（仅 `plan_version=pro` 生效） | 相似度阈值（0.0–1.0），低于此值的结果被过滤，默认 `0.3`。 | **强烈建议调优**：`0.5–0.7` 平衡查准率与查全率；`<0.4` 易召回噪声，`>0.8` 易漏检。 |
| `profile_schema` | ⚠️（仅写入用户画像时必需） | `CreateProfileSchema` 返回的 schema ID。需提前创建模板，定义字段名、类型及提取策略。 | 模板字段应精简（≤10 个核心属性），避免过度抽取；`extract_scene` 推荐 `"efficient"`（同步）或 `"intelligent"`（异步，需配 `/add-async`）。 |
| `memory_library_id` / `project_id` | ❌（可选） | 指定目标记忆库或项目空间，用于多租户/多业务线隔离。未传则使用账号默认库。 | 多业务场景（如电商+客服）建议为每个业务创建独立 `memory_library_id`，便于权限与用量管控。 |

> 💡 **开发者提示**：  
> - 写入优先用 `AddMemoryAsync`：高吞吐、含图片/长文本时更可靠，避免同步超时；  
> - 检索必设 `min_score`：`pro` 策略下不设该参数等于放弃质量过滤；  
> - `user_id` 是安全边界：切勿将不同用户混用同一 `user_id`，否则导致记忆污染；  
> - 限流需主动处理：`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM，超限返回 `429`，务必实现指数退避（1s→2s→4s→8s）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [security guide](../guides/security-guide.md)
- [llm application](../guides/llm-application.md)


