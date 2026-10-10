# 记忆机制

记忆机制是百炼平台为大模型应用提供的跨会话、结构化、可检索的长期状态管理能力，用于突破模型上下文窗口限制，实现对话连贯性、用户个性化与任务连续性。它不依赖模型参数微调，而是通过独立服务（记忆库）与标准化 API，在推理前将相关历史信息按语义注入 Prompt，形成“带记忆的上下文”。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）场景**：  
  - *Agent 2.0 / Managed Agents*：通过 `resources.memory_store` 挂载记忆库，系统在每次推理前自动检索并注入匹配记忆片段；支持与工具调用、多步规划协同，例如基于“用户昨日提交的代码报错日志”自动复现并调试。  
  - *Flow Agent*：在控制台 Agent 配置页一键绑定记忆库，启用后所有对话自动触发事实记忆提取与画像更新，无需修改提示词或代码逻辑。

- **工作流（Workflow）场景**：  
  使用 OpenClaw 等记忆插件节点，或直接调用记忆 API（如 `/memory_nodes/search`），在任意节点（如条件判断、大模型节点前）注入动态记忆。适用于需精细控制记忆注入时机与范围的编排逻辑，例如仅在“售后服务”分支中加载用户历史投诉记录。

- **高代码应用（Rich Code Application）场景**：  
  开发者可直接集成 `dashscope` SDK 或调用 REST API（`https://dashscope.aliyuncs.com/api/v2/apps/memory/`），在自定义 Python 逻辑中完成记忆写入（`/add`）、异步画像查询（`/user_profile`）与混合检索（`/search?memory_source=fact&profile_schema_id=xxx`），实现与业务系统深度耦合的记忆闭环。

- **安全与治理场景**：  
  记忆读写操作默认受平台内生安全防护覆盖——记忆库资源自动纳入 Agent 资产盘点，高级防护策略可检测并告警“异常批量记忆导出”“敏感字段未脱敏写入”等风险行为，保障记忆数据隔离性与合规性。

## 关键参数和配置

| 参数 | 说明 | 推荐值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 记忆归属标识，强制用于数据隔离 | 必填（建议使用业务侧稳定 ID，如 `uid_12345`） | 不同 `user_id` 完全物理隔离；不可为空或占位符（如 `"default"`） |
| `plan_version` | 检索/写入策略版本 | `Pro`（精度优先）或 `Lite`（成本优先） | `Search` 请求可独立指定，与写入规则无关；`Pro` 启用 Rerank，质量更高 |
| `top_k` | 单次检索返回的最大记忆条数 | `5–10` | 超过 `20` 易引入噪声；Managed Agents 中默认为 `5`，API 默认为 `10` |
| `min_score` | 相似度阈值（浮点数 `0.0–1.0`） | `0.5–0.7` | `0.0` 表示不过滤（慎用）；`1.0` 仅返回完全匹配项；OpenClaw 插件需转换为整数 `0–100`（如 `0.6 → 60`） |
| `memory_source` | 注入类型（仅限 LTM 原生注入模式） | `"fact"` 或 `"profile"` | 混合使用需分两次请求；`qwen-max`/`plus`/`turbo` 模型才支持该字段 |
| `enable_long_term_memory` | 是否启用 LTM 上下文注入 | `true`（显式开启） | 默认 `false`；未设此字段则记忆不会注入到模型输入中 |
| `ttl_seconds` | 记忆有效期（秒） | `604800`（7 天）或 `2592000`（30 天） | `fact` 默认 30 天，`profile` 默认 7 天；`0` 表示永不过期（不推荐） |

> ⚠️ **重要一致性提醒**：  
> - 所有 REST API（含 `/add`, `/search`, `/user_profile`）均要求 `min_score` 为 `0.0–1.0` 浮点数；  
> - OpenClaw 插件等少数封装层接受整数 `0–100`，调用前请自行转换（`int(min_score * 100)`）；  
> - `profile_schema_id` 仅在需触发结构化用户画像抽取时必传，否则仅处理事实记忆。

## 面向开发者，简洁实用

- ✅ **快速验证三步走**：  
  ```bash
  # 1. 写入（自动提取事实+画像）
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{"user_id":"uid_123","messages":[{"role":"user","content":"我叫张三，30岁，喜欢 hiking"}],"profile_schema_id":"ps_abc123"}'

  # 2. 检索（语义召回）
  curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{"user_id":"uid_123","messages":[{"role":"user","content":"我的爱好是什么？"}],"min_score":0.6,"top_k":3}'

  # 3. 注入模型（LTM 原生模式）
  curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -d '{
          "model": "qwen-max",
          "messages": [...],
          "long_term_memory": {
            "enable_long_term_memory": true,
            "memory_source": "fact",
            "max_memory_items": 10
          }
        }'
  ```

- ✅ **生产建议**：  
  - 事实记忆优先配置 `plan_version=Pro` + `min_score=0.6`，平衡精度与成本；  
  - 用户画像务必预定义 `profile_schema` 并传入 `profile_schema_id`，避免非结构化噪声；  
  - Managed Agents 中挂载记忆库后，无需额外调用 API，平台自动完成检索与注入；  
  - 记忆写入后立即可检索（事实记忆），但画像需等待 2–5 秒再查 `GET /user_profile`；  
  - 定期调用 `/memory_nodes/clear` 清理测试数据，生产环境建议设置 `ttl_seconds` 自动过期。

- ❌ **避坑指南**：  
  - 不要省略 `user_id` —— 否则写入失败或混入默认库；  
  - 不要对非 `qwen-max`/`plus`/`turbo` 模型设置 `enable_long_term_memory=true` —— 字段被忽略；  
  - 不要传入超长 `fact` 内容（>512 字符）—— API 返回 `400`；  
  - 不要依赖记忆 100% 召回 —— 高可靠性场景建议结合业务 ID 显式查询（如 `GET /memory_nodes?user_id=xxx&tag=order_id_789`）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [security guide](../guides/security-guide.md)
- [llm application](../guides/llm-application.md)


