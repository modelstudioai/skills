# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的跨会话、结构化、语义驱动的记忆持久化与检索能力，用于突破大模型单次推理的上下文长度限制，实现用户事实信息、行为偏好与画像特征的自动提取、长期存储与高相关性召回。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆不是单一功能模块，而是贯穿多个平台能力的横切基础设施，其使用方式因集成路径和应用范式而异：

- **在 Memory Library（记忆库）中**：作为独立服务提供，通过 `AddMemory` / `SearchMemory` 等开放 API 显式管理。支持两类记忆类型：  
  - **事实记忆（Fragments）**：从对话消息中自动提取可验证的离散事实（如“每天9点喝水”），适用于动态、时效性信息；  
  - **用户画像（Profiles）**：基于预定义 schema 结构化抽取稳定属性（如“职业=设计师，偏好=简洁回复”），支持异步生成与查询。  
  可通过 Agent Harness 一键启用，或通过 OpenClaw 插件在工作流中全自动捕获与注入（`before_agent_start` → `agent_end` 钩子驱动）。

- **在 LLM Application（智能体/工作流）中**：作为增强能力嵌入应用生命周期。调用已发布的智能体时，通过请求参数 `memory_id` 指定关联的记忆库 ID，平台自动完成检索与 Prompt 注入；该能力仅对新版智能体（Agent 2.0）及部分旧版智能体生效，工作流暂不原生支持。

- **在 Model-Level API（模型直调）中**：需配合标注 `ltm_enabled: true` 的专用模型（如 `qwen-max-20241017`, `qwen3-max` 等）使用。通过 `parameters.memory.{write, read}` 控制写入与读取行为，系统自动判别内容类型并分发至事实库或画像库，无需手动指定。

- **在 Managed Agents 中**：作为上下文扩展资源挂载，与文件、工具环境并列。记忆库以“跨会话持久化文件树”的抽象形式提供状态复用能力，支撑长时运行任务中的上下文连续性（如多轮代码调试、迭代式数据分析）。

> ⚠️ 注意：基础模型（如 `qwen-turbo`）或未显式启用 LTM 的模型，即使传入 `memory` 参数也不会触发任何持久化或检索行为。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 默认值 | 建议值 |
|------|----------|------|--------|--------|
| `user_id` | Memory Library API / LTM Model API | 记忆隔离维度，不同 `user_id` 数据完全隔离 | 必填 | 业务侧唯一用户标识（如 UUID 或登录 ID） |
| `memory_id` | Application Call（智能体调用） | 绑定已创建的记忆库 ID，启用自动检索注入 | 可选 | 控制台创建记忆库后获得的 `memory_id` 字符串 |
| `plan_version`（`Pro` / `Lite`） | Memory Library | 控制 Rerank 是否开启，影响精度与成本 | `Pro` | 高精度场景用 `Pro`；高频低敏感场景可用 `Lite` |
| `top_k` | Memory Library API / LTM Model API | 单次检索最大返回条数 | `10`（API） / `5`（插件） / `5`（model-level） | `3–5`（平衡效果与噪声）；上限 `100` |
| `min_score` / `fact_threshold` / `profile_threshold` | Memory Library（`min_score`） / Model API（`*_threshold`） | 相似度阈值（0.0–1.0），低于则过滤 | `0.3` / `0.65` / `0.72` | `0.5–0.7`（通用推荐）；`profile_threshold` 可略高于 `fact_threshold` |
| `expires_at` | Memory Library API / LTM Model API | ISO8601 格式时间戳，显式设置 TTL | 无（永不过期） | 显式传入（如 `"2025-12-31T23:59:59Z"`）以实现精准过期控制 |
| `profile_schema` | Memory Library（用户画像） | 用户画像模板 ID，启用结构化抽取 | 可选 | 调用 `CreateProfileSchema` 后获取 |

> 💡 提示：记忆默认**永不过期**，除非显式配置 `expires_at` 或在控制台记忆规则中设置过期时间；文档中提及的“默认180天”仅为初始规则模板值，非全局强制策略。

## 面向开发者，简洁实用

- ✅ **快速验证**：开通 Memory Library 后，直接调用 `AddMemory` 写入含 `user_id` 和 `messages` 的对话，再用 `SearchMemory` 检索，无需额外配置即可体验。
- ✅ **零侵入集成**：OpenClaw 工作流中安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，配置 `apiKey` 和 `userId`，启用 `autoCapture`/`autoRecall`，Agent 自动完成全链路记忆管理。
- ✅ **模型直调最简用法**：
  ```json
  {
    "model": "qwen-max-20241017",
    "input": { "messages": [{"role":"user","content":"我的生日是1992年5月3日"}] },
    "parameters": {
      "memory": { "write": true, "read": true, "fact_threshold": 0.7 }
    }
  }
  ```
- ✅ **避坑指南**：
  - 不要对非 `ltm_enabled` 模型使用 `memory` 参数；
  - 流式响应（`stream: true`）下 `memory.write` 不生效，请改用同步模式；
  - 记忆内容严格按 `app_id + user_id` 隔离，跨应用/跨用户数据不可见；
  - `memory.read: true` 不自动过滤低分或过期记忆，需结合 `min_score` 或主动清理。

- 📈 **容量注意**：单应用上限为 100 万条事实记忆 + 10 万条用户画像；超限时写入返回 `400 QuotaExceeded`，建议定期归档或按需清理。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)


