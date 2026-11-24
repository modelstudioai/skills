# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、企业微信、钉钉、微信公众号等高频触点，并提供云端与本地双模 RAG 应用构建能力。所有方案均基于统一的大模型应用（App）和知识库（Knowledge Base）抽象，通过 AppFlow 低代码连接流实现渠道适配，开发者可复用核心 Prompt、知识库和评测流程，显著降低多端部署成本。

## 支持的模型/功能

- **基础模型**：默认推荐 `Qwen3.5-Plus`（文档1）、`千问-Plus`（文档2、3、4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档4中用于提速）。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定（如 `你叫小助...`）、多轮对话、工具调用（隐式）；
  - RAG 增强：通过知识库实现私有文档问答，支持文件上传、切片检索、相似度阈值控制（文档1、2、3、4）；
  - 多端交互渲染：网站悬浮挂件、企业微信应用、钉钉机器人卡片、微信公众号被动/主动消息（文档1–4）；
  - 本地 RAG 支持：允许知识检索环节在本地执行，生成环节调用百炼 API，适用于对数据主权或文档预处理灵活性要求高的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档1中明确指定模型为 `Qwen3.5-Plus`，而文档2、3、4统一使用 `千问-Plus`。二者为同一模型的不同命名（Qwen3.5-Plus 即千问-Plus），无实质差异；但文档4在“常见问题”中建议未认证公众号用户改用 `qwen-turbo` 以满足 5 秒响应限制，此为特定场景下的模型降级策略，非通用推荐。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源示例 |
|----------|--------|------|----------|
| **身份凭证** | `App ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `API Key` | 百炼调用密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| | `AgentKey`（业务空间标识） | 用于校验智能体与 API Key 是否同属一个业务空间，排查 `request error` 的关键字段 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| **RAG 控制** | `调用方式` | 知识库调用策略，如 `必定调用`（强制检索）、`按需调用`（模型自主判断） | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |
| | `相似度阈值` | 过滤召回片段的最低语义相似度，范围通常为 0–1，0 表示不过滤 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **生成控制** | `温度（temperature）` | 控制输出随机性，值越高越发散，生产环境建议设为 0.1–0.5 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `最大回复长度（max_tokens）` | 限制模型输出 token 数，影响回答详略程度 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **统一建模**：在百炼控制台创建**智能体应用**，配置 Prompt、选择模型、发布应用；
2. **知识注入**：通过[数据连接](https://bailian.console.aliyun.com/?tab=app#/connector/list)上传文件 → [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建 → 在应用配置中启用并绑定知识库；
3. **渠道集成**：
   - **网站**：使用 AppFlow 创建 AI 助手 → 配置 Web 集成 → 获取悬浮挂件脚本 → 插入 HTML；
   - **企业微信/钉钉/微信公众号**：在对应平台创建应用（获取 `CorpID/AgentID/ClientID` 等）→ 使用 AppFlow 预置模板创建连接流 → 绑定百炼应用与平台凭证 → 配置 Webhook 或消息接收地址；
4. **日志与监控**：可在 AppFlow 连接流中添加 SLS 日志节点，记录对话上下文用于分析 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。

## 限制和注意事项

- **免费额度**：新用户可享百炼[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用；但 AppFlow、函数计算 FC、ADB-PG 向量存储等依赖服务单独计费；
- **响应时效约束**：
  - 微信公众号未认证时，被动回复必须在 **5 秒内完成**，超时即失败（文档4）。此时应选用 `qwen-turbo` 或精简 Prompt；
  - 企业微信/钉钉无硬性超时，但建议优化知识库切分与嵌入质量以降低延迟；
- **安全与合规**：
  - 企业微信要求配置**可信 IP**，若使用第三方代理（如 AppFlow 默认出口），需启用“内网代理”并配置自有 ECS 或 Nginx 实例（文档2）；
  - 微信公众号配置服务器 URL 时若报“安全风险”，需改用服务商授权模式（文档4）；
- **知识库限制**：
  - 云端知识库单文件 ≤ 100 MB 或 1000 页，支持格式包括 `.pdf`, `.docx`, `.txt`, `.xlsx` 等（文档2）；
  - 本地 RAG 方案虽无上传限制，但受限于 Embedding API 限流，不建议单次传入 >100 MB 文件（文档5）；
- **调试要点**：出现 `request error` 或 `Failed to stream content` 时，优先检查 `API Key` 状态、`App ID` 正确性、`AgentKey`（业务空间）一致性（文档1）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


