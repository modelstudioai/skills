# 应用调用、应用组件与知识服务API对比

为帮助开发者在百炼平台中高效选型，本文系统对比三类核心AI能力接口：**应用调用（[application call](../api/application-call.md)）**、**应用组件（application component）** 和 **知识服务（[knowledge](../api/knowledge.md)）**。三者定位不同——应用调用面向已封装的业务级智能体/工作流复用；应用组件面向模型原语级控制与自定义编排；知识服务则聚焦结构化知识的检索与问答闭环。本对比基于当前（2024年Q3）正式发布能力，覆盖协议设计、功能边界、部署约束及工程实践要点，旨在为架构设计、MVP验证与生产集成提供技术决策依据。

## 关键维度对比

| 维度 | 应用调用（[application call](../api/application-call.md)） | 应用组件（application component） | 知识服务（[knowledge](../api/knowledge.md)） |
|------|-----------------------------|-----------------------------------|------------------------|
| **核心定位** | 调用已发布的**完整应用实例**（Agent/Workflow），开箱即用业务逻辑 | 调用**基础大模型能力**，支持[函数调用](../concepts/function-calling.md)、多轮对话等原语，需自行编排流程 | 提供**知识增强专用能力**：语义检索（search）与端到端RAG问答（chat），深度集成知识库策略 |
| **输入格式** | • DashScope API：`prompt`（单轮）或 `messages`（多轮）+ `image_list`/`file_list`<br>• Responses API（OpenAI兼容）：`input` 数组，支持 `input_text`/`input_image`/`input_file` 类型 | 标准 OpenAI `messages` 数组（含 `role`/`content`），支持 `tools` 工具定义数组；不支持原生多模态文件输入（如图片/音视频） | • 检索：`query`（文本）或 `images`（URL列表）或两者混合<br>• 问答：`input.messages`（DashScope标准格式），**必须流式**（`stream=true`） |
| **输出格式** | • 同步：JSON 响应（含 `output.text`、`thought`、`memory_id` 等）<br>• 流式：SSE（DashScope）或 chunked JSON（Responses）<br>• 异步：返回 `task_id`，需轮询结果 | • 同步：标准 OpenAI-style JSON（含 `choices[0].message.content`、`tool_calls`）<br>• 流式：SSE，按 `delta` 分块<br>• 异步：通过 `/v1/jobs/{id}` 获取结果 | • 检索：JSON，`data.nodes[]` 包含切片（`text`, `score`, `metadata`）<br>• 问答：SSE，`event: message` 帧含 `extra.group`（planning/tool_calling/generating）和 `extra.step`，错误以 `event: error` 返回 |
| **支持模型** | • 不直接暴露模型选择<br>• 功能由应用配置决定：新版Agent 2.0 / 旧版Agent / Workflow<br>• 多模态依赖应用内启用（VL/Audio模型需应用配置支持） | 显式指定 `model` 参数：<br>• `qwen-max` / `qwen-plus` / `qwen-turbo`（公测）<br>• `qwen-vl` / `qwen-audio`（暂未开放公测） | • **不暴露模型参数**<br>• 模型由控制台发布的 `agent_config` 决定（向量模型、混排模型、NL2SQL模型等）<br>• 问答阶段自动调度 `semantic_search`、`obtain_file` 等内置工具 |
| **API 端点** | • DashScope 原生：<br> `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• Responses（OpenAI兼容）：<br> `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST https://<region-id>.bailian.aliyuncs.com/api/v1/chat/completions`<br>（区域 ID 如 `cn-beijing`、`ap-southeast-1`） | • 检索：<br> `POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`<br>• 问答：<br> `POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/knowledge/chat` |
| **认证方式** | Header `Authorization: Bearer {DASHSCOPE_API_KEY}` | • RAM AccessKey 鉴权（`X-Acs-AccessKeyId` + `X-Acs-Signature`）<br>• 或 `Authorization: Bearer <access_token>`（OAuth2 Token） | Header `Authorization: Bearer <API-Key>`（独立知识服务API Key） |
| **计费方式** | 按调用次数 + 输出 token 计费<br>• 同步/异步调用均计费<br>• 流式响应按实际输出 token 计费 | 按输入+输出 token 总数计费<br>• 同步/流式/异步任务统一按 token 计费<br>• 工具调用本身不额外计费，但调用产生的模型推理计入 token | 按调用次数计费<br>• 检索：每次请求计 1 次<br>• 问答：每次流式会话计 1 次（无论内部调用多少次工具）<br>• **不按 token 计费** |
| **典型场景** | • 客服机器人（集成RAG+[长期记忆](../concepts/long-term-memory.md)+多轮对话）<br>• 自动化工作流触发（如审批→通知→归档）<br>• 多模态报告生成（上传PDF+截图→分析→生成摘要） | • 构建自定义LLM Router（路由至不同模型）<br>• 实现复杂工具链（如“查天气→订机票→发邮件”）<br>• 需精细控制 [prompt](../guides/prompt.md) engineering 与输出 schema 的场景 | • 企业知识库搜索（文档/表格/图片联合检索）<br>• 对话式知识助手（用户问“上季度销售TOP3产品”，自动SQL查询+图表生成）<br>• 面向非技术用户的零代码知识交互入口 |
| **地域与Workspace支持** | • 所有路径**仅支持华北2（北京）地域**<br>• 子空间（Workspace）通过 `X-DashScope-WorkSpace` Header 传递，用于调用跨地域模型（如东京/法兰克福） | • 支持多地域（`cn-beijing`、`ap-southeast-1` 等）<br>• Workspace 通过 endpoint 中的 `region-id` 体现，**无独立 Workspace ID 传参** | • Endpoint 中显式包含 `{workspaceId}.cn-beijing`，**强制绑定北京地域**<br>• Workspace 是服务前置条件，无跨地域模型支持 |

## 适用场景建议

### ✅ 选择「应用调用」当：
- 你已有在百炼控制台**发布完成的智能体或工作流**，且其功能（RAG、记忆、多模态）完全满足业务需求；
- 需要**快速上线生产服务**，避免重复开发对话管理、状态维护、插件调度等基础设施；
- 业务强依赖**长期用户记忆**（如记住客户偏好）或**多轮上下文感知**（如导购对话）；
- 团队以产品/业务为主导，希望低代码集成AI能力。

### ✅ 选择「应用组件」当：
- 你需要**完全掌控模型调用链路**，例如动态切换 `qwen-plus` 与 `qwen-max`、自定义 tool calling 逻辑、或注入私有工具；
- 正在构建**通用AI中间件**（如统一LLM网关），需抽象模型层而非应用层；
- 场景对**token成本敏感**，需精确控制输入长度与输出上限（`max_tokens`）；
- 需要**跨地域部署**（如新加坡用户调用 `ap-southeast-1` 接入点），且不依赖百炼预置应用能力。

### ✅ 选择「知识服务」当：
- 核心诉求是**知识驱动的精准检索或可信问答**，而非通用对话；
- 知识源已结构化入库（文档、数据库、表格），且需**开箱支持NL2SQL、多跳推理、图文混合搜索**；
- 希望将知识能力**解耦为独立微服务**，供多个前端（App/Web/小程序）复用；
- 运维要求高：需明确知道每次问答只计1次调用，成本可预测，无需核算token。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **是否需要多模态（图像/音视频）原生支持？** | 应用调用 > 知识服务 > 应用组件 | 应用调用通过 `image_list`/`file_list` 直接支持；知识服务支持图文混合检索；应用组件当前不开放 `qwen-vl`/`qwen-audio` 公测。 |
| **是否需[长期记忆](../concepts/long-term-memory.md)（跨会话用户画像）？** | 应用调用（唯一支持） | 仅应用调用提供 `memory_id` 参数，自动管理记忆生命周期；其他两类均无状态持久化能力。 |
| **是否需自定义工具调用逻辑？** | 应用组件（最灵活） > 应用调用（受限于应用配置） > 知识服务（固定工具集） | 应用组件允许任意定义 `tools` 并控制 `tool_choice`；应用调用的工具由应用内配置决定；知识服务仅提供预置工具（`semantic_search`, `obtain_file`）。 |
| **是否需严格控制 token 成本？** | 应用组件（最透明） > 应用调用 > 知识服务 | 应用组件按实际 token 计费且可设 `max_tokens`；应用调用虽按 token 计费但受应用内部逻辑影响（如RAG召回内容计入输入）；知识服务按次计费，成本恒定但不可控输出长度。 |
| **是否需跨地域部署？** | 应用组件（支持） > 应用调用 / 知识服务（仅北京） | 应用组件接入点支持 `cn-beijing`/`ap-southeast-1`/`eu-central-1` 等；另两者Endpoint硬编码北京地域，无法变更。 |
| **是否需与现有OpenAI SDK无缝集成？** | 应用调用（Responses API） ≈ 应用组件 | 应用调用提供 OpenAI 兼容 Responses API；应用组件原生遵循 OpenAI API 规范；知识服务为百炼专属协议（SSE帧结构特殊）。 |
| **是否需最小化运维负担？** | 应用调用（最高） > 知识服务 > 应用组件 | 应用调用由百炼托管全部运行时（记忆、RAG、流式）；知识服务托管检索与问答引擎；应用组件需自行处理会话状态、错误重试、限流熔断等。 |

> **重要提醒**：  
> - 所有API均需通过百炼控制台**开通对应服务权限**并获取有效凭证（API Key / AccessKey / Workspace ID）；  
> - 生产环境务必实现**限流降级**：应用调用与知识服务默认25 QPS，应用组件依地域配额而定；  
> - 调试优先使用控制台「API调试」功能，避免因Header缺失（如 `X-DashScope-WorkSpace`）或地域错配导致404/403；  
> - 多模态场景请严格校验文件URL有效性与CORS策略，百炼不代理文件下载。

## 被对比主题页

- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [knowledge](../api/knowledge.md)


