# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话的记忆管理服务，用于持久化存储用户关键事实与画像信息，并在后续对话中基于语义检索自动注入上下文，从而突破模型上下文窗口限制，实现个性化、连贯的智能体交互。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）场景**：在 Managed Agents 中，可通过 `resources.memory_store` 挂载记忆库，赋予智能体“记住用户偏好”“延续多轮任务状态”的能力；调用时自动触发 `autoRecall`（检索注入）与 `autoCapture`（对话结束提取），无需手动拼接 Prompt。  
- **应用调用（Application Call）场景**：新版智能体应用支持 `memory_id` 参数，启用后平台自动关联用户 `user_id`，完成记忆写入与检索闭环，开发者仅需传参，无需调用底层 Memory API。  
- **工作流与插件场景**：通过 OpenClaw 等插件集成，可将长期记忆作为独立节点嵌入流程，支持条件触发（如仅当用户首次提问时写入画像）、多规则混合检索（`project_ids`）等高级编排。  
- **RAG 增强场景**：与知识库协同使用——RAG 提供领域知识，长期记忆提供用户专属上下文（如“张三讨厌咖啡因”），二者共同注入 [prompt](../guides/prompt.md)，提升响应准确性与个性化水平。  
- **安全防护场景**：所有记忆读写操作默认经过内容安全检测（含敏感词、PPI 识别等），确保存储与检索过程符合数据合规要求。

## 关键参数和配置

| 参数 | 说明 | 必填 | 典型值/约束 |
|------|------|------|-------------|
| `user_id` | 记忆归属唯一标识，用于隔离用户数据，所有接口必需 | ✓ | 字符串，≤64 字符，建议业务侧生成（如 `uid_12345`） |
| `plan_version` | 控制检索质量策略 | ✗ | `"Pro"`（默认，启用 Rerank，精度高）、`"Lite"`（跳过 Rerank，延迟低）；大小写不敏感 |
| `min_score` | 相似度阈值，过滤低相关结果 | ✗ | `0.0–1.0`，推荐 `0.5–0.7`；设为 `0.3` 可放宽召回，`0.8` 适用于高精度场景 |
| `top_k` | 单次检索最大返回条数 | ✗ | `1–100`，默认 `10`；智能体场景建议 `5–15`，平衡信息量与 token 开销 |
| `project_id` / `project_ids` | 记忆规则作用域标识 | ✗ | 单规则用 `project_id`，多规则混合检索用 `project_ids: ["p1","p2"]` |
| `profile_schema` | 用户画像模板 ID（仅写入时生效） | ✗ | 传入则触发结构化抽取；不传仅存事实记忆 |

> ⚠️ 注意：`user_id` 是记忆隔离的唯一维度，**不支持按 session_id 或 app_id 隔离**；同一 `user_id` 下所有应用共享该用户记忆（除非显式配置多 project 隔离）。

## 面向开发者，简洁实用

- **快速上手**：3 行代码完成闭环  
  ```python
  # 1. 写入（同步）
  client.add_memory(user_id="u123", messages=[{"role":"user","content":"每天9点提醒喝水"}])
  # 2. 检索（带当前对话上下文）
  res = client.search_memory(user_id="u123", messages=[{"role":"user","content":"今天要做什么？"}], top_k=5)
  # 3. 注入 prompt（示例）
  prompt = f"用户历史偏好：{res['memory_nodes'][0]['content']}\n当前问题：今天要做什么？"
  ```

- **异步写入适用长对话/多模态**：对 >50 轮对话或含图像/文件的输入，优先用 `/add-async`，通过 `event_id` 轮询结果，避免超时。

- **用户画像需主动创建模板**：先调用 `CreateProfileSchema` 定义字段（如 `{"name":"age","description":"用户年龄"}`），再在 `AddMemory` 中传 `profile_schema`，约 3 秒后调 `GetUserProfile` 获取结果。

- **调试技巧**：  
  - 控制台「记忆检索」页实时调参（`top_k`/`min_score`/开启改写），立即验证效果；  
  - 所有 API 响应含 `request_id`，错误时结合 [错误码文档](https://help.aliyun.com/zh/bailian/developer-reference/error-codes) 排障；  
  - 限流失败（HTTP 429）必须实现指数退避重试（建议 base=100ms，max=2s）。

- **生产注意事项**：  
  - 记忆默认永不过期，**务必为时效性信息显式设置过期时间**（如“会议预约”设 7 天）；  
  - 删除记忆库将**永久清除所有内容且不可恢复**，删除前请确认；  
  - 免费额度将于 **2026 年 8 月 20 日 10:00（北京时间）** 结束，之后按实际调用量计费。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [security guide](../guides/security-guide.md)


