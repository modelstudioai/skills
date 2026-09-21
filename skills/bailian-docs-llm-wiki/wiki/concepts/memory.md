# 长期记忆

长期记忆是百炼平台提供的跨会话、结构化、可检索的持久化记忆服务，用于突破大模型单次对话的上下文限制，将用户交互中产生的关键信息（如动态事实与稳定画像）自动提取、存储并按需召回，实现真正个性化的连续智能体验。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：通过 Agent Harness 零代码配置启用 `autoCapture`（对话结束自动写入）和 `autoRecall`（对话开始前自动检索注入），无需修改提示词即可增强记忆感知能力；适用于客服助手、个人助理等需长期理解用户意图的场景。  
- **工作流（Workflow）应用**：在 OpenClaw 等可视化流程中，通过「长期记忆插件」节点调用 `AddMemory` / `SearchMemory`，支持在任意环节写入或检索记忆（例如：用户提交偏好后立即更新画像，后续问答前注入相关事实）。  
- **高代码（Rich Code）应用**：开发者直接集成 DashScope SDK，调用 `/add`（同步）或 `/add-async`（长对话/多模态）写入记忆，并在 `chat_completions.create` 前手动调用 `/memory_nodes/search` 获取结果，注入 Prompt 实现精准上下文增强。  
- **Managed Agents**：通过挂载 `memory_store` 类型资源，将长期记忆作为可读写的文件树供智能体沙箱直接访问（如 `read /memory/profile.json`），适用于需本地化处理记忆数据的复杂任务（如生成用户周报、分析行为趋势）。  
- **知识库增强场景**：与 RAG 协同使用——长期记忆承载“用户专属事实”（如“张三对咖啡因敏感”），知识库承载“通用领域知识”，二者在 Prompt 中分层注入，避免语义混淆，提升回答准确性与个性化水平。

## 关键参数和配置

| 参数 | 说明 | 推荐值/约束 | 备注 |
|------|------|-------------|------|
| `user_id` | 记忆归属唯一标识，必填 | 字符串，≤64 字符 | 不同 `user_id` 数据完全隔离；建议与业务用户 ID 对齐 |
| `profile_schema` | 用户画像模板 ID | 字符串（如 `"50edf54e..."`） | **不传则跳过画像提取**；仅当需结构化属性（年龄/职业/爱好）时传入 |
| `messages` / `custom_content` | 输入内容源（互斥） | `messages`: ≤50 条对话；`custom_content`: ≤512 字符纯文本 | 优先用 `messages` 以保留角色语义；`custom_content` 适合日志、表单等非对话输入 |
| `plan_version` | 检索与抽取策略版本 | `"Pro"`（默认，启用重排/Rerank）或 `"Lite"`（低成本） | 影响 `SearchMemory` 结果质量与延迟；`Pro` 更适合高精度场景 |
| `top_k` | 单次检索最大返回条数 | `1–100`，默认 `10` | 结合 Token 成本权衡：`top_k=3` 适合轻量注入，`top_k=20` 适合重排后精筛 |
| `min_score` | 相似度阈值 | `0.0–1.0`，建议 `0.5–0.7` | `<0.5` 易引入噪声；`>0.7` 可能漏召关键记忆；调试时可在控制台「记忆检索」页实时验证 |

> ⚠️ 注意：`project_ids`（数组）支持跨项目混合检索，但与 `project_id`（单值）互斥；`skill_name`/`skill_description`/`skill_tags` 仅在注册 Skill 类型记忆时必需。

## 面向开发者，简洁实用

- **快速上手三步**：① 控制台开通记忆库 → ② 调用 `POST /add` 写入（带 `user_id` + `messages`）→ ③ 调用 `POST /memory_nodes/search` 检索（带 `user_id` + `query`），结果手动注入 Prompt。  
- **必做检查**：写入画像时确认 `profile_schema` 已创建且 ID 正确；检索前确保 `plan_version` 与业务需求匹配（高精度选 `Pro`）；异步写入后需轮询 `/events/{event_id}` 获取完成状态。  
- **避坑提示**：`SearchMemory` 返回内容计入模型上下文 Token，需预留足够窗口；`DeleteMemory` 不可逆，生产环境慎用；`user_id` 是隔离核心，切勿混用。  
- **调试利器**：控制台「记忆详情」页可按 `user_id` 查看所有记忆；「记忆检索」页支持实时调整 `top_k`/`min_score` 并预览结果，无需反复发 API。  
- **计费提醒**：记忆库本身按存储量+调用量计费（2026年8月20日10:00起生效），但 `SearchMemory` 注入的上下文 Token 将额外产生模型调用费用，需在成本预算中单独计算。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [start using](../guides/start-using.md)


