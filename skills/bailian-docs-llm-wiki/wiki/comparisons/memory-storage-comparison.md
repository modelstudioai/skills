# 知识库、记忆库与长期记忆对比

本文档面向大模型应用开发者，旨在对比百炼平台三大上下文增强方案的核心差异与架构边界。在构建企业级 AI 应用时，开发者常面临“如何高效注入外部知识”与“如何维持跨会话对话连续性”的选型难题。通过系统梳理**知识库**、**记忆库**与**长期记忆（新）**的输入输出形态、检索机制、API 路径及计费模型，帮助团队在 RAG 问答、个性化 Agent 或复杂意图延续等场景中做出精准的技术决策。

## 🔍 核心维度对比

| 对比维度 | 知识库 (Knowledge Base) | 记忆库 (Memory Library) | 长期记忆（新）(Long Term Memory New) |
|:---|:---|:---|:---|
| **核心定位** | 基于 RAG 的私有/业务数据语义检索，解决知识滞后与幻觉 | 突破上下文窗口限制，跨会话沉淀关键事件与用户属性 | 面向 Agent 的全生命周期记忆节点管理，提供高精度检索与强干预管线 |
| **输入格式** | 结构化/非结构化文档（PDF/Word/音视频等）、Metadata/Tags | `messages` 数组（完整多轮）、`custom_content`、预定义 Schema | `messages` (≤50条) 或 `custom_content` (≤512字符，强互斥)、`meta_data` |
| **输出/存储形态** | 智能切分语义片段（≤6000 Token）、重排序候选集 | 记忆片段（Memory Fragment）、结构化用户画像（User Profile） | 记忆节点（Memory Node）、经 Rerank/Rewrite/Judge 过滤的高优上下文 |
| **支持模型** | 千问全系(QwQ/Max/Plus/Turbo/Long/VL)、DeepSeek、Llama 及[[微调]]模型 | 依赖底层 LLM 自动抽取，兼容主流[[llm-model]]注入 | 结合[[画像模板]]体系，面向 Agent 架构优化，支持意图判别回调 |
| **API 端点/集成方式** | 控制台直接挂载 / [[工作流应用]]拖拽节点 / 标准上传注册链路（申请租约→OSS→索引轮询） | `AddMemory` / `SearchMemory` / `modelstudio-memory-for-openclaw` 插件自动钩子 | RESTful 路由：`POST /memory/add`、`POST /memory_nodes/search` / `agentscope-runtime>=1.1.5` SDK |
| **计费方式** | **双轨计费**：实例规格费（按运行时长）+ 向量/排序模型 Token 费（**按初步召回 TopK 总量计费**） | 按 API 调用频次与底层向量/抽取模型 Token 计费，受 QPM 配额约束 | 同记忆库计费逻辑，严格遵循账号级总 QPM ≤ 3000，高频需退避重试 |
| **典型场景** | 垂直领域政策问答、技术文档检索、多模态（图文/音视频）内容理解 | 跨会话个性化服务、轻量级用户偏好沉淀、自动化对话上下文保持 | 高精度意图延续、复杂 Agent 状态管理、需强过滤与 Query 优化的业务流 |
| **关键限制** | 创建后类型/切分策略**不可逆**；多路召回按 N 倍消耗 Token；欠费有 8~14 天清理期 | `SearchMemory` 延迟约 200~500ms；单库规则上限 50 条；TTL 需业务侧自行维护 | `messages` 与 `custom_content` 强互斥；部分接口（如 Update）SDK 暂未原生封装；当前无自动归档机制 |

## 🛠️ 技术选型与场景建议

| 业务特征 | 推荐方案 | 架构建议 |
|:---|:---|:---|
| **需检索企业静态文档、产品手册、最新业务公告** | [[知识库]] | 开启智能切分与重排序，针对复杂 Query 调高 `Final TopK`（≤20）。建议配合 `Metadata/Tags` 实现部门/产品线级路由过滤。 |
| **需记住用户历史偏好、基础信息，实现“千人千面”对话** | [[记忆库]] | 利用插件 `auto_capture`/`auto_recall` 实现无感注入。若依赖强规则属性，务必传入 `profile_schema` 进行结构化抽取，避免纯语义漂移。 |
| **Agent 需高精度控制上下文、支持口语化 Query 改写与意图强过滤** | [[长期记忆（新）]] | 开启 `enable_rewrite` 提升召回，搭配 `enable_judge` 拦截低相关性节点。注意将高频写入收敛至批量处理或使用指数退避策略。 |
| **混合架构：既要查公司政策，又要记用户习惯** | **知识库 + 长期记忆** | 工作流中并行挂载：知识库处理客观事实召回，长期记忆注入主观偏好。通过 Prompt 模板明确优先级（如“优先遵循记忆库中的用户指令”）。 |

## 💡 开发注意事项
1. **路径与版本对齐**：记忆相关 API 在演进过程中存在端点差异（如 `/memory/search` 与 `/memory/memory_nodes/search`）。生产环境集成务必以控制台提供的最新 SDK 或 [[长期记忆（新）API 参考]] 为准。
2. **性能与延迟权衡**：长期记忆开启 `enable_rewrite` 可显著提升口语 Query 召回率，但会引入约 `50~100ms` 额外延迟。对实时性要求极高的流式场景，建议通过 A/B 测试确定最优开关组合。
3. **生命周期治理**：平台当前对记忆片段与用户画像**暂无自动失效机制**。开发者应结合业务 TTL 策略，定期调用分页清理接口，避免向量池膨胀导致检索精度衰减与成本上升。

📚 **延伸阅读**  
- [[知识库]] · [[知识库 API 指南]]  
- [[记忆库概览]] · [[为 OpenClaw 配置长期记忆插件]]  
- [[长期记忆（新）API 参考]] · [[长期记忆（新）]]

## 被对比主题页

- [[knowledge-base|knowledge base]] — `../guides/knowledge-base.md`
- [[memory-library-overview|memory library overview]] — `../guides/memory-library-overview.md`
- [[long-term-memory-new|long term memory new]] — `../api/long-term-memory-new.md`

