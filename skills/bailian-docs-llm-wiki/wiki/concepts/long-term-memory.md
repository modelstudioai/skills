# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的**结构化、持久化、跨会话的智能体记忆管理服务**，用于存储和检索用户事实、技能知识与结构化画像三类高价值上下文信息，支撑智能体实现真正的状态延续与个性化演进。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发（Managed / Flow / Sandbox Agent）**：作为 `agent context` 的核心组件之一，通过 `context_type="memory"` 注入会话上下文。仅对同一 `user_id` + `session_id` 有效，支持在多轮对话中自动关联历史偏好、任务进度或用户身份特征；需配合 `context_id`（即 `project_id`）指定记忆空间，确保不同业务模块（如“客服”“订单”“学习助手”）的记忆物理隔离。

- **RAG 增强场景**：与 Knowledge（知识库）形成互补——Knowledge 存储静态、通用、批量导入的文档资料；而 Long Term Memory 存储动态、个性化、实时生成的用户专属数据（如“张三上周投诉过物流延迟”“李四偏好简体中文回复”），二者可通过 `context_list` 同时注入，实现“通用知识 + 个性记忆”的联合推理。

- **Agent 治理与可观测性**：所有 `AddMemory` / `SearchMemory` 调用均自动上报为 OpenTelemetry Trace 事件，出现在 Agent 全链路追踪中（标注为 `memory.write` / `memory.search`），支持监控耗时、成功率、命中率及内容安全检测结果，是诊断“记忆未生效”“画像更新延迟”等问题的关键观测维度。

- **CLI 工具集成**：通过 `bl memory add` 和 `bl memory search` 命令直接操作记忆库，适用于离线批量初始化用户画像、调试记忆抽取效果或构建自动化评测流水线；支持 `--async` 异步提交与 `--follow` 阻塞等待，与平台 API 行为完全一致。

- **多模态智能体**：当项目配置启用多模态能力时，传入 `messages` 中的 `image_url` 将参与记忆抽取（如从用户上传的证件照中识别性别/年龄/证件类型），否则图片内容被静默忽略；该行为由 `project_id` 对应的记忆规则控制，无需额外开关。

## 关键参数和配置

| 参数 | 必填 | 说明 | 推荐值/约束 |
|------|------|------|-------------|
| `user_id` | ✅ | 用户唯一标识，用于跨会话、跨 Agent 的记忆隔离 | 字符串，建议与业务系统 ID 对齐（如 `"uid_123456"`） |
| `project_id` 或 `project_ids` | ✅ | 记忆所属业务空间；决定记忆类型（`observation`/`skill`）及抽取规则；异步接口支持最多 5 个 | `"proj-customer-service"`；`project_ids` 与 `custom_content` 互斥 |
| `extract_mode` | ⚠️ | 抽取策略：`efficient`（低延迟，同步接口专用）、`intelligent`（高精度，**必须用异步接口**） | 生产环境默认 `intelligent`；实时轻量写入可用 `efficient` |
| `profile_schema` | ❌（画像场景必填） | 用户画像模板 ID，触发结构化画像抽取与更新 | 需提前调用 `CreateProfileSchema` 创建；传入后 `memory_types` 不生效 |
| `plan_version` | ❌ | 计费与能力版本：`pro`（支持 `min_score` 过滤、Rerank）、`lite`（基础检索） | 默认 `pro`；`search` 时若需 `min_score`，必须设为 `pro` |
| `memory_types` | ❌（检索时） | `SearchMemory` 指定检索的记忆类型，默认 `["observation"]`；**不支持 `user_profile`** | `["observation", "skill"]`；`user_profile` 需单独调用 `GetUserProfile` |
| `top_k` / `min_score` | ❌（检索时） | `top_k` 控制返回条数（默认 5，最大 50）；`min_score`（仅 `plan_version=pro`）过滤低置信度结果 | `top_k=10`, `min_score=0.75` |

> 💡 **关键实践提示**：
> - `intelligent` 模式下**严禁使用同步 `AddMemory`**，必须走 `AddMemoryAsync` → `GetEvent` 流程，否则必然超时；
> - `user_profile` 是独立数据模型，**不能通过 `SearchMemory` 查询**，必须使用 `GetUserProfile`；
> - 所有写入均默认持久化、无自动过期；如需 TTL 管理，请在业务层自行标记时间戳并定期清理。

## 面向开发者，简洁实用

- **快速上手**：  
  ```bash
  # 写入一条事实记忆（高效模式）
  bl memory add --user-id user_001 --project-id proj-support \
                --messages '[{"role":"user","content":"我想退订会员"}]' \
                --extract-mode efficient

  # 异步写入技能记忆（推荐生产用）
  EVENT_ID=$(bl memory add-async --user-id user_001 --project-ids '["proj-onboarding"]' \
                                  --messages '[{"role":"assistant","content":"调用cancel_subscription工具"}]' \
                                  --extract-mode intelligent --json | jq -r '.event_id')
  bl memory get-event --event-id $EVENT_ID --follow
  ```

- **检索示例**：  
  ```bash
  bl memory search --user-id user_001 --project-id proj-support \
                   --messages '[{"role":"user","content":"上次我反馈的问题解决了吗？"}]' \
                   --memory-types '["observation"]' --top-k 3 --plan-version pro
  ```

- **错误处理**：  
  - HTTP 429（限流）：按指数退避重试（1s → 2s → 4s）；  
  - HTTP 400（参数错误）：检查 `user_id`/`project_id` 格式、`profile_schema` 是否存在、`memory_types` 是否含 `user_profile`；  
  - `GetUserProfile` 返回空：首次调用需等待 `AddMemoryAsync` 完成且画像抽取成功，建议业务侧加 1~3 秒重试逻辑。

- **性能与成本**：  
  - 账号级总限流 3000 QPM（`add` ≤120 QPM，`search` ≤300 QPM）；  
  - `plan_version=pro` 支持高级能力但计费更高，`lite` 仅适用于低敏感度场景；  
  - 记忆库将于 **2026-08-20 10:00（北京时间）起正式计费**，请提前规划用量。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [agent governance](../guides/agent-governance.md)
- [agent context](../guides/agent-context.md)
- [capabilities](../guides/capabilities.md)


