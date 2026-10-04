# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的跨会话、结构化、语义可检索的记忆管理能力，用于持久化存储用户事实性信息与画像特征，并在后续对话中自动注入相关上下文，突破大模型单次请求的上下文窗口限制。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆不是单一功能模块，而是贯穿多个平台能力的横切基础设施，按使用方式可分为三类：

- **Agent Harness 原生集成**（推荐）：在智能体（Agent 2.0）或 Managed Agents 中启用 `enable_memory: true`，平台自动完成记忆写入（基于对话内容提取）与检索（语义召回），无需手动调用 API。适用于需要“开箱即用”记忆能力的智能体应用。
  
- **插件/工作流集成**：通过「长期记忆插件」接入工作流（Workflow）或 OpenClaw 等低代码编排环境，支持配置 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索），适合需精细控制触发时机的流程型应用。

- **API 直接调用**：通过 `AddMemory` / `SearchMemory` 等 REST API 或 `agentscope-runtime` SDK 手动管理记忆，适用于高代码应用（如 Serverless Function）、自定义 RAG 流程或需与外部系统（如 CRM）双向同步的场景。

> ✅ 统一前提：所有路径均要求稳定传入 `user_id`（符合规范：1–64 字符，仅含字母、数字、`_`、`-`），否则记忆无法跨会话关联或写入失败。

## 关键参数和配置

| 参数 | 说明 | 取值/范围 | 注意事项 |
|------|------|-----------|----------|
| `user_id` | 记忆归属标识，强制隔离不同用户数据 | 字符串（1–64 字符，仅含 `[a-zA-Z0-9_-]`） | **必填**；同一用户所有调用必须一致，否则视为不同实体 |
| `memory_library_id` | 指定目标记忆库（用于多业务隔离） | 字符串 | 不传则使用账号默认记忆库（不可删除） |
| `plan_version` | 决定检索质量与计费版本 | `"Pro"`（默认） / `"Lite"` | `Pro` 启用重排序（Rerank），精度高；`Lite` 成本低，适合简单匹配；**事实记忆与用户画像的 Lite 单价不同（¥0.018 vs ¥0.025/次）** |
| `top_k` | 检索返回的最大记忆条数 | `1–100` | 默认 `10`；增大可提升召回率，但增加 [Token](token.md) 消耗与延迟 |
| `min_score` | Pro 版相似度阈值（仅 `SearchMemory` 生效） | `0.0–1.0` | 建议 `0.5–0.7`；过低引入噪声，过高漏召 |
| `memory_config.type` | API 场景下指定记忆类型（仅限 `enable_memory=true` 时） | `"fragments"`（事实记忆） 或 `"profiles"`（用户画像） | **不可混用**；两类记忆需独立配置、独立调用 |
| `memory_config.ttl_seconds` | 记忆项存活时间（TTL） | 整数（秒），默认 `604800`（7 天） | 设为 `0` 表示永不过期（不推荐生产环境） |

> ⚠️ 重要约束：  
> - 用户画像需预先调用 `CreateProfileSchema` 定义字段模板，并在 `AddMemory` 中传入 `profile_schema` ID 才生效；  
> - 画像提取为异步过程，`AddMemory` 返回后需等待数秒再调用 `GetUserProfile`；  
> - 单次 API 请求最多触发 **1 次事实记忆写入 + 1 次用户画像更新**，不支持批量操作。

## 面向开发者：快速上手建议

1. **验证通路（3 分钟）**：  
   ```bash
   # 1. 写入记忆（替换 YOUR_API_KEY 和 USER_ID）
   curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/AddMemory \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "USER_ID",
           "messages": [{"role":"user","content":"我叫张三，28岁，工程师，每天9点喝水"}]
         }'

   # 2. 检索记忆（相同 user_id）
   curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/SearchMemory \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "USER_ID",
           "messages": [{"role":"user","content":"提醒我喝水"}],
           "top_k": 3
         }'
   ```

2. **生产部署要点**：  
   - 优先创建**独立记忆库**（非默认库），避免多业务相互干扰；  
   - 为用户画像配置明确 `profile_schema` 并预置初始标签（如通过 `/v1/memory/profiles/upsert`）；  
   - 在 Agent 或 Workflow 中启用 `autoRecall` 时，务必设置合理 `top_k` 和 `min_score`，防止低质记忆污染 Prompt；  
   - 监控 `SearchMemory` 调用量与平均 `top_k`，平衡效果与成本。

3. **调试技巧**：  
   - 使用控制台「记忆详情」页按 `user_id` 查看提取结果，验证规则是否生效；  
   - 在 `agenteval` 观测中检查 `memory_read` / `memory_write` Trace 节点，定位检索为空或写入失败原因；  
   - 若检索无结果，优先检查 `user_id` 是否一致、`plan_version` 是否匹配、`min_score` 是否过高。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [agenteval](../guides/agenteval.md)


