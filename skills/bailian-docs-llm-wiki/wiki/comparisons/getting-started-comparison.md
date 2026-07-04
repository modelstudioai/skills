# 入门路径对比：开始使用与模型快速上手

阿里云百炼同时面向"应用构建者"和"模型调用开发者"两类用户，提供了两条不同的入门路径。`start-using` 侧重于在控制台零代码搭建基于私有知识的问答应用（智能体应用、工作流应用、知识库等）；`get-started-with-models` 则侧重于通过兼容 OpenAI 的 API 直接调用大模型完成第一次推理。本页从目标用户、输入形式、输出形式、支持模型、API 端点、计费方式、典型场景等维度对比两条路径，帮助开发者根据需求做出技术选型。

## 关键维度对比

| 维度 | [start using](../guides/start-using.md)（应用构建路径） | [get started with models](../guides/get-started-with-models.md)（模型调用路径） |
| --- | --- | --- |
| 主要目标 | 零代码/低代码搭建端到端的私有知识问答应用 | 通过 API 直接调用大模型完成文本/多模态推理 |
| 目标用户 | 业务人员、应用开发者、希望快速上线 RAG 应用的团队 | 开发者、需要将模型推理集成到自有代码或后端服务的工程师 |
| 上手时长 | 约 5 分钟完成第一个智能体应用（含知识库构建） | 几行代码即可完成首次调用，开通账号后即可跑通 |
| 输入形式 | 控制台可视化配置：System Prompt、知识库、技能、MCP 工具、工作流节点 | HTTP 请求 / OpenAI 兼容 SDK / DashScope SDK，传入 `messages`、`model`、参数 |
| 输出形式 | 发布后的应用（Web、微信、钉钉、音视频实时互动）+ Responses API 同步/异步调用 | 模型推理结果（文本、图像、音频、视频、向量、重排序结果） |
| 应用类型 | 智能体应用（Agent 2.0）、工作流应用、高代码应用、MCP 服务 | 直接调用模型 API；可叠加模型调优（SFT/CPT/DPO）、模型部署、模型评测 |
| 支持模型 | 千问系列（推荐 qwen3.7-max 用于问答）、QwQ 推理系列、DeepSeek 系列、视觉模型 qwen-vl-plus/max、嵌入 text-embedding-v3/v4 | 文本生成（qwen3.7-max/plus、qwen3.6-flash、deepseek-v4-pro/flash、kimi-k2.7-code、glm-5.2 等）、图像/视频/3D/音频/全模态/向量/重排序全谱系 |
| 知识库 | 核心能力：文档/数据/图片/音视频知识库、智能切分、检索调优、图文检索、监控 API | 不直接提供知识库；如需 RAG 需自行搭建或与百炼应用/知识库集成 |
| API 端点 | Responses API（同步 + `background=true` 异步），调用时需传入自定义参数；通过应用 ID 调用 | OpenAI 兼容 `/compatible-mode/v1`、Anthropic 兼容地址、DashScope SDK 端点；按计费方案选择 Base URL |
| 接入域名 | 应用调用走百炼统一接入，发布渠道含微信/钉钉/音视频 SDK | 业务空间专属 `{WorkspaceId}.{region}.maas.aliyuncs.com`（生产推荐）、`dashscope.aliyuncs.com`（存量）、`trial.{region}.maas.aliyuncs.com`（验证）、Token/Coding Plan 专属域名 |
| 凭证与鉴权 | 控制台操作为主；API 调用时使用应用相关凭证 | API Key（按业务空间隔离，不可跨地域混用）；建议写入环境变量 `DASHSCOPE_API_KEY` |
| 地域选择 | 应用开发与批量推理、模型调优仅在北京与新加坡支持 | 多地域可选（北京、新加坡、法兰克福、东京、弗吉尼亚），地域决定接入点与数据存储；服务部署范围可限定中国内地/国际/全球 |
| 计费方式 | 大模型调用计费 + 知识库规格费用 + 知识库模型调用费用（2026-01-04 起正式计费）；提供限时免费额度 | 按量付费（Dashscope 域名 / 业务空间专属 / 试用域名）、Token Plan（交互式，不可用于后端）、Coding Plan（AI 编码套餐）；不同方案对应不同 Base URL |
| 调用模式 | 同步调用（实时交互，可复用 OpenAI 代码库）、异步调用（`background=true` 返回 Task ID） | 同步、流式（SSE）、批量推理、异步任务；请求超时最高 3600 秒（业务空间专属域名） |
| 可观测性 | 应用观测（端到端流程）、应用评测（智能体/工作流/自定义评测集）、长期记忆与用户画像 | 模型告警（仅北京/新加坡）、模型评测、模型调优 |
| 典型交付物 | 可对外发布的问答应用（含欢迎语、预设问题、发布渠道、音视频互动） | 一次模型推理调用或集成了模型能力的后端服务 |

## 适用场景建议

### 选择 [start using](../guides/start-using.md)（应用构建路径）当：

- 需要在 5 分钟内零代码搭建一个能回答私有领域问题的问答应用。
- 业务方或非工程师角色希望可视化配置 System Prompt、知识库、技能、MCP 工具。
- 需要完整 RAG 流程（知识库构建、切分策略、检索调优、图文检索）且不想自行实现。
- 需要发布到微信、钉钉、H5/APP 等渠道，或需要音视频实时互动。
- 需要端到端应用观测、评测、长期记忆与用户画像管理。

### 选择 [get started with models](../guides/get-started-with-models.md)（模型调用路径）当：

- 开发者需要将大模型推理直接集成到自有代码、后端服务或 AI 工作流中。
- 需要使用 OpenAI 兼容 SDK 或 DashScope SDK，复用现有 OpenAI 代码库。
- 需要访问文本、图像、视频、3D、音频、全模态、向量/重排序等完整模型谱系。
- 对地域、服务部署范围、接入域名、并发上限、SLA 有精细控制需求。
- 需要使用 Token Plan / Coding Plan 等专项计费方案，或需要进行模型调优（SFT/CPT/DPO）、模型部署、模型评测。

### 两条路径结合使用：

实际项目中两条路径常常互补——先用 `get-started-with-models` 跑通模型调用、选定合适模型与地域，再用 `start-using` 将模型能力封装为带知识库、技能、发布渠道的完整应用；反过来，已发布的应用也可通过 Responses API 被后端服务以 OpenAI 兼容方式调用。开发者可先明确"我要的是模型推理能力还是端到端应用"，再据此选择起点。

## 来源主题页

- [start using](../guides/start-using.md)（guides/start-using.md）
- [get started with models](../guides/get-started-with-models.md)（guides/get-started-with-models.md）

## 被对比主题页

- [start using](../guides/start-using.md)
- [get started with models](../guides/get-started-with-models.md)


