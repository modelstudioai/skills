# RAG 与[长期记忆](../concepts/long-term-memory.md)能力对比

本页旨在为百炼平台开发者提供 **RAG（[检索增强生成](../concepts/rag.md)）能力** 与 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）能力** 的系统性对比分析，帮助技术团队在构建智能体（Agent）、知识密集型应用或上下文感知服务时，准确理解二者在定位、能力边界、集成方式及成本模型上的本质差异，从而做出符合业务目标与工程约束的技术选型决策。

> ⚠️ 重要提示：RAG 与[长期记忆](../concepts/long-term-memory.md) **并非互斥替代关系，而是互补协同关系**。RAG 侧重“外部知识的按需调用”，长期记忆侧重“内部经验的持续沉淀”。实际高阶 Agent 架构中，二者常联合使用（例如：用 LTM 维护用户画像与操作习惯，用 RAG 检索产品文档与 SOP 流程）。

---

## 关键维度对比

| 维度 | RAG API | 长期记忆（LTM） |
|------|---------|----------------|
| **核心定位** | 外部知识库的语义化检索与问答服务，面向**静态/半静态结构化/非结构化知识资产**（如文档、表格、图片、音视频） | 内部运行时记忆的结构化管理服务，面向**动态生成的、用户/会话/任务相关的事实、技能与画像数据**（如对话历史摘要、工具调用经验、偏好标签） |
| **输入格式** | • 知识库创建：支持 `file`（PDF/DOCX/CSV/JSON 等）、`url`、`text`、`image`、`audio/video`<br>• 运行时检索/问答：`query`（文本）、`images`（Base64 或 URL）、`input.messages`（完整对话历史，含 role/content） | • 写入：`messages`（对话数组，用于抽取 observation/skill）、`custom_content`（纯文本）、`profile_schema`（画像模板 ID）<br>• 检索：`messages`（查询语句）、`project_ids`（指定记忆类型归属）、`user_id`（强制隔离） |
| **输出格式** | • 检索接口 `/search`：返回 `chunks`（带 score 的语义片段）、`documents`（原始文档元信息）<br>• 问答接口 `/chat`：SSE 流式响应，含 `answer`、`references`（引用片段）、`trace_id`；支持 `tool_calls`（当启用 Agent 工具链） | • 写入（同步）：直接返回 `memory_nodes` 数组（含 `id`, `type`, `content`, `metadata`）<br>• 写入（异步）：返回 `event_id`，需轮询获取结果<br>• 检索 `/search`：返回 `memory_nodes` 列表（含 `score`, `type`, `content`, `project_id`）<br>• 用户画像：`GET /user_profile` 返回结构化 JSON（如 `{"age": 32, "interests": ["AI", "travel"]}`） |
| **支持模型/能力** | • 嵌入模型：`text-embedding-v4`, `qwen3-vl-embedding` 等可配置<br>• 重排序模型：`qwen3-rerank`（可自定义）<br>• Agent 模型：`qwen3.7-plus` 等大模型驱动问答<br>• 多模态：原生支持 `image_qa`, `visual_perception_qa`, `multimedia` 场景 | • 抽取模型：由平台统一调度（不暴露模型名），分 `lite`/`pro` 计划版本<br>• `pro` 版本支持重排序（`min_score` 过滤）、联合画像+技能抽取<br>• 不依赖外部大模型完成写入/检索，但抽取过程隐式调用平台推理服务 |
| **API 端点（Base URL）** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>• 管理类：`/api/v1/rag/...`<br>• 运行时：`/api/v1/indices/knowledge/search`, `/api/v2/apps/knowledge/chat` | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`<br>• 写入：`/add`, `/add-async`<br>• 检索：`/memory_nodes/search`<br>• 画像：`/profile_schemas`, `/user_profile` |
| **认证方式** | `Authorization: Bearer <API-Key>`（使用百炼控制台生成的 **API Key**） | `Authorization: Bearer $DASHSCOPE_API_KEY`（使用百炼控制台生成的 **DashScope API Key**，注意密钥类型不同） |
| **计费方式** | • 按调用量计费：<br> – 文档解析、切片、嵌入向量化（按 token/页数）<br> – 检索调用（按次）<br> – 问答调用（按 token 输出 + 模型调用）<br>• 无明确免费额度，具体见[百炼定价页](https://help.aliyun.com/zh/bailian/pricing) | • **商业化起始时间：2026年8月20日 10:00（北京时间）**<br>• 分 `Lite` 与 `Pro` 版本：<br> – `Lite`：基础写入/检索，无重排序<br> – `Pro`：支持 `min_score` 过滤、高级抽取、画像联合建模<br>• 计费项：`Add` 调用次数、`Search` 调用次数（按 QPM 配额外用量计费） |
| **数据生命周期** | • 知识库/文档/切片默认**永久存储**（除非显式删除）<br>• 支持软删除，但无自动过期策略<br>• 数据所有权归属业务空间，跨空间不可见 | • 记忆节点默认**永久持久化**，无自动过期机制<br>• 删除为软删除（`status=delete`），历史记录仍可查<br>• `user_id` 强隔离，保障多租户数据安全 |
| **典型场景** | • 客服知识库问答（PDF/SOP 文档）<br>• 表格数据分析助手（Excel/CSV 查询）<br>• 图片内容理解（商品图识别、医疗影像报告生成）<br>• 音视频内容检索（会议录像关键片段定位） | • 用户个性化推荐（基于历史交互提炼兴趣标签）<br>• Agent 自我优化（记录成功/失败的工具调用路径，形成 `skill` 记忆）<br>• 对话状态管理（跨会话维护用户意图、待办事项、偏好设置）<br>• B2C 应用中的实时用户画像构建与更新 |

---

## 各方案适用场景建议

### ✅ 推荐优先选用 **RAG API** 当：
- 你的知识源是**预先准备好的、相对稳定的外部资料**（如企业制度文档、产品手册、API 文档、历史工单库）；
- 需要**多模态支持**（尤其是图像、音视频等非文本内容的语义理解）；
- 业务对**检索精度与上下文相关性要求极高**，且愿意为嵌入/重排序/大模型问答支付相应成本；
- 应用形态为“**查知识、答问题、做分析**”，而非持续学习与行为演化。

### ✅ 推荐优先选用 **长期记忆（LTM）** 当：
- 你需要让 Agent **从每次交互中持续学习并积累经验**（例如：记住用户说“我不喜欢推送通知”，下次自动关闭）；
- 必须构建**强用户身份绑定的个性化能力**（如金融场景中动态更新风险偏好、投资目标）；
- 需要将**工具调用过程结构化沉淀为可复用技能**（如“订会议室”流程固化为 `skill` 节点，供后续自动编排）；
- 对**低延迟写入有硬性要求**（同步 `add` 接口适用于轻量事实记录），或能接受异步处理以换取高稳定性（主推 `add-async`）；
- 希望规避大模型幻觉对关键记忆的影响——LTM 的 `observation` 和 `user_profile` 是**确定性结构化数据**，非生成式内容。

### ⚖️ 推荐 **联合使用 RAG + LTM** 当：
- 构建企业级智能助手：用 **RAG 提供权威知识底座**（如 HR 政策、IT 故障处理指南），用 **LTM 记录员工个性化信息与历史请求模式**（如“张三常在周五下午申请远程办公”）；
- 开发自动化 Agent：用 **LTM 存储已验证的 `skill` 流程**（如“审批报销单”的完整步骤），用 **RAG 检索最新财务制度条款** 作为执行依据；
- 实现“越用越懂你”的 C端应用：**LTM 维护用户画像与短期意图**，**RAG 实时检索兴趣领域最新资讯/教程**，共同驱动个性化内容生成。

---

## 面向开发者的技术选型参考

| 选型考量点 | RAG API | 长期记忆（LTM） | 建议动作 |
|------------|---------|------------------|----------|
| **是否需要管理自有知识资产？** | ✅ 是（必须上传/导入文档/媒体） | ❌ 否（记忆来自运行时交互） | 若无现成知识库，RAG 需额外投入文档治理成本 |
| **是否要求跨会话保持用户上下文？** | ⚠️ 有限（仅靠 `/chat` 输入 `messages` 传递历史，易受长度限制） | ✅ 强支持（`user_id` + 持久化 `observation`/`user_profile`） | 高度依赖用户状态的应用（如个人助理、健康管家）首选 LTM |
| **是否需多模态理解能力？** | ✅ 原生支持 image/audio/video 场景 | ❌ 仅支持文本输入（`messages`/`custom_content`） | 涉及视觉/听觉交互的产品必须选 RAG |
| **是否关注记忆的可解释性与可控性？** | ⚠️ 片段引用可追溯，但问答结果受大模型影响 | ✅ 所有记忆节点为结构化 JSON，字段含义明确，可审计、可编辑、可删除 | 合规敏感场景（如金融、医疗）建议用 LTM 存储关键事实，RAG 仅作辅助检索 |
| **工程复杂度与 SDK 支持** | 中等：需处理 `index_id`/`agent_id` 命名不一致、流式响应解析、切片管理逻辑 | 较低：SDK（`agentscope-runtime`）封装完善，异步事件模型清晰，错误码体系统一 | 新项目建议优先评估 SDK 封装程度，降低接入门槛 |
| **未来扩展性** | 适合横向扩展知识库规模（支持千万级文档） | 适合纵向深化记忆粒度（支持 observation/skill/profile 三级抽象） | 规划 3 年以上演进路径时，建议架构预留双通道接入能力 |

> 💡 **一句话总结选型原则**：  
> **“用 RAG 接入世界，用 LTM 记住用户”** ——  
> 若你的应用核心价值在于**连接权威知识**，选 RAG；  
> 若核心价值在于**理解并适应特定用户**，选 LTM；  
> 若两者皆重，请设计 **RAG + LTM 协同架构**，并在 Agent 编排层明确分工（例如：先查 LTM 获取用户画像，再用 RAG 检索匹配该画像的知识片段）。

---  
*最后更新：2025年4月*  
*文档状态：正式版（v1.2）*

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


