# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API、代码执行环境、内容生成服务等）标准化接入推理流程，弥补大模型在实时信息获取、精确计算、确定性执行和[多模态](multi-modal.md)生成等方面的固有局限。每个插件本质上是一个可被模型识别、规划并调用的结构化工具。

## 在百炼平台的不同场景中，这个概念如何使用

插件在百炼平台中并非独立运行单元，而是作为“工具”被不同应用形态按需编排与调用，具体方式如下：

- **智能体应用（Agent）**：在 Agent 2.0 中，插件与知识库、MCP 工具统一纳入“工具空间”，由大模型自主进行**规划-调用-反思**。例如用户提问“对比 A 和 B 产品的最新价格并画成柱状图”，模型可自动选择 `quark_search` → `code_interpreter` → `text_to_image` 串联执行。官方插件需在控制台“插件市场”添加至目标智能体（同业务空间内），最多支持 10 个。

- **工作流应用（Workflow）**：插件以独立节点形式拖入画布，作为**确定性执行单元**参与编排。不依赖模型决策，开发者可精确控制其输入、上下游依赖及失败重试策略。适用于需强流程保障的场景，如“先调用 `calculator` 验证参数，再触发 `github_search` 检索 SDK 版本”。

- **Assistant API / Managed Agents API**：通过 `tools` 字段声明可用插件列表（如 `["calculator", "text_to_image"]`），平台在推理过程中自动注入工具描述，并在模型输出 `tool_calls` 后完成 HTTP 调用与结果回填。自定义插件需先发布为 MCP 服务，并在 API 请求中通过 `biz_params` 透传业务级参数（如用户 ID、租户上下文）。

- **与 Skill、Connector 的关系**：  
  - *Skill* 侧重文件驱动的自动化任务（如“解析 PDF 并提取表格”），基于 ZIP 包+语义描述，运行于沙箱；  
  - *Connector* 是企业级数据源网关，通过 MCP 协议将数据库、OSS、SaaS 等系统能力封装为工具集；  
  - *插件* 是更轻量、更通用的工具抽象，覆盖计算、搜索、生成等原子能力，既包含官方预置（如 `code_interpreter`），也支持 OpenAPI 自定义。三者可共存于同一智能体，由模型按需调度。

## 关键参数和配置

- **工具 ID**：唯一标识符（如 `calculator`, `python_interpreter`），用于 API 声明与控制台关联，区分大小写，不可重复。

- **输入参数（Input Schema）**：  
  - 必须明确定义 `name`、`description`、`type`（String/Number/Object）、`in`（`path`/`query`/`body`）；  
  - `Object` 类型子属性**不能为空**，且 `GET` 请求不支持 `Object` 输入（会导致发布失败）；  
  - `传参方式` 分两类：`大模型识别`（模型从用户输入中抽取值）或 `业务透传`（开发者通过 `biz_params` 固定传入，如 `{"user_id": "u123"}`）。

- **输出参数（Output Schema）**：  
  - 所有字段必填，用于指导模型解析响应；  
  - 建议扁平化设计（避免深层嵌套），字段名应语义清晰（如 `result_summary` 而非 `data.res.sum`）。

- **鉴权配置（仅自定义插件）**：  
  - 支持 `Header` 或 `Query` 方式；  
  - `Type` 可选 `basic`/`bearer`/`appcode`；  
  - **注意**：仅 `Authorization` Header 可透传，其他自定义 Header（如 `X-Trace-ID`）会被平台丢弃。

- **启用开关**：在 API 调用时，需显式在 `tools` 数组中声明 ID；未声明则模型无法感知该工具存在。

## 面向开发者，简洁实用

- ✅ **快速验证**：控制台调试插件时，务必点击“在线测试”并确认返回状态码 200 + JSON 格式响应，否则发布后无法启用。  
- ✅ **参数安全**：敏感参数（如 API Key）严禁硬编码，应通过 `biz_params` 传入，并配合 Vault 加密存储。  
- ✅ **错误定位**：若插件未被调用，检查三点：① `tools` 数组是否包含正确 ID；② 输入参数是否满足 `required` 字段约束；③ 模型是否具备该插件调用能力（仅 `qwen-turbo` 及以上模型支持）。  
- ⚠️ **限制红线**：  
  - `code_interpreter` 禁止网络请求、文件上传、系统命令执行；  
  - `quark_search` 仅返回结构化摘要，不提供原始网页内容；  
  - 删除插件将**永久清除其下所有工具**，已关联应用立即失效；  
  - 修改 URL 或鉴权配置后，必须重新测试并发布，否则调用失败。  
- 🚀 **推荐实践**：优先使用官方插件（开箱即用、免运维）；自定义插件建议从简单 REST API 入手，逐步增加鉴权与复杂参数，避免一上来集成 OAuth 或 Webhook。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)
- [overview](../guides/overview.md)
- [application support](../guides/application-support.md)
- [skill](../guides/skill.md)
- [managed agents api](../api/managed-agents-api.md)


