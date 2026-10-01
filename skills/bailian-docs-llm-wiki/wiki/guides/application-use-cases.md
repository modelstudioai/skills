# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业通讯与业务平台中，实现开箱即用的 AI 助手、智能客服或机器人。当前已验证的典型场景包括在企业微信、微信公众号、钉钉和网站中嵌入 RAG 增强型问答应用，所有方案均基于统一的百炼应用底座，通过 AppFlow 无代码连接流完成平台对接，无需自行部署推理服务或向量数据库。核心能力聚焦于私域知识问答、7×24 客户咨询响应与业务流程自动化辅助。

## 支持的模型/功能

- **基础模型**：推荐使用 `qwen-plus`（平衡效果/速度/成本），亦支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）及 `qwen3.5-plus`（文档 2 明确指定）；[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中明确建议该模型为本场景最优选。
- **RAG 增强**：所有场景均支持通过知识库注入私有文档（PDF/DOCX/TXT/CSV 等），启用[检索增强生成](../concepts/rag.md)。知识库可存储于云端（标准版/ADB-PG 向量库）或本地（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **交互形式**：支持文本对话、卡片消息（钉钉）、悬浮挂件（网站）、群聊/私聊机器人（企业微信/钉钉/微信公众号）。
- **扩展能力**：支持日志记录（SLS）、自定义前端样式、多轮对话上下文控制、DeepSeek 思考过程展示（钉钉专属）等高级功能。

> **注意**：文档 1 与文档 2 在模型选择上存在差异——文档 1 推荐 `qwen-plus`，文档 2 明确推荐 `qwen3.5-plus` 并说明其定位介于 Max 与 Flash 之间。实际选型应以最新控制台可用模型为准，`qwen3.5-plus` 为当前更优默认选项。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | 温度（temperature） | 控制输出随机性，值越高越发散 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的“修改模型参数”章节 |
| | 最大回复长度（max_tokens） | 限制生成 token 数量 | 同上 |
| | 携带上下文轮数 | 控制历史对话记忆深度 | 同上 |
| **RAG 层** | 召回片段数（top_k） | 检索返回的最相关文本段数量 | 同上 |
| | 相似度阈值（similarity_threshold） | 过滤低于该相似度的检索结果 | 同上；也见文档 1/5 的“知识”区域配置 |
| **应用层** | Prompt | 定义角色、任务边界与输出格式（如“请总是给出简短的回答”） | 所有文档的“应用配置”或“Prompt设置”步骤 |
| | 调用方式 | 知识库调用策略：`必定调用` / `按需调用` | 文档 1/2/3/5 的“引用知识”步骤 |

## 使用方式

1. **创建百炼应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择模型、配置 Prompt，发布应用并获取 `AppID` 与 `API Key`。
2. **准备知识源（可选但推荐）**：
   - 上传文件至百炼数据连接或文件中心；
   - 创建知识库并关联文件；
   - 在应用配置中开启知识库开关，选择目标知识库及调用方式。
3. **配置目标平台接入**：
   - **企业微信/钉钉/微信公众号**：使用 AppFlow 预置模板（文档 1/3/5 提供具体 URL），配置平台凭证（CorpID/AgentID/Secret 或 AppID/ClientID）与百炼凭证，生成 Webhook URL。
   - **网站**：通过 AppFlow → 模型服务AI助手 → Web页面集成，生成悬浮挂件脚本，嵌入 HTML 即可。
4. **平台侧配置**：
   - 企业微信：配置 API 接收消息（填入 Webhook URL、Token、EncodingAESKey）与可信 IP；
   - 钉钉：在应用开发后台启用 HTTP 模式机器人，填入 Webhook URL；
   - 微信公众号：完成服务器配置（URL + Token + EncodingAESKey），认证用户需额外处理白名单与菜单接口；
   - 网站：粘贴挂件脚本，支持拖拽、预置问题等 UI 定制。
5. **验证与迭代**：在目标平台发起测试对话，结合 [应用评测](../../raw/application-user-guide/agenteval/agenteval-introduction.md) 流程优化 Prompt 或知识库切分策略。

## 限制和注意事项

- **平台认证要求**：微信公众号未认证时仅支持被动回复（5 秒超时限制），认证后方可使用客户消息接口实现异步响应；企业微信/钉钉需对应组织管理员权限开通开发者能力。
- **文件限制**：云端知识库单文件 ≤ 100 MB 或 1000 页，图片 ≤ 20 MB；本地 RAG 应用不建议上传 > 100 MB 文件（受限于 Embedding API 限流）。
- **网络与安全**：
  - 企业微信/钉钉/微信公众号均要求配置可信 IP 白名单，AppFlow 会提供所需 IP 列表；
  - 微信公众号配置服务器时若报“URL 存在严重安全风险”，需改用服务商授权模式重新创建连接流；
  - 域名主体校验失败（企业微信）需配置自有备案域名或通过 Nginx 代理转发（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 的“常见问题”章节）。
- **调试要点**：若出现 `request error` 或无响应，优先检查三项是否一致：API Key 状态、AppID 正确性、API Key 与智能体是否在同一业务空间（文档 2 的“常见问题”明确列出）。
- **计费说明**：百炼 API 调用按 token 计费；AppFlow、函数计算（FC）、ADB-PG 等依赖服务单独计费，非百炼平台内费用。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


