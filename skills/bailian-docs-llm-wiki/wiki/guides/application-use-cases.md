# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心是将大模型能力与业务系统（如企业微信、钉钉、微信公众号、网站等）通过低代码/无代码方式集成，并结合 RAG 技术接入私有知识。所有方案均基于统一的百炼应用模型服务，通过 AppFlow 实现跨平台连接流编排，开发者只需关注模型配置、知识库构建和业务系统对接三类关键动作。

## 支持的模型/功能

- **基础模型**：支持 `qwen-plus`（文档 1、3、4 中默认推荐）、`qwen3.5-plus`（文档 2 明确指定）、`qwen-max` 和 `qwen3.5-flash`（文档 5 列出可选模型），各模型在效果、速度、成本上存在权衡，需按场景选择。
- **核心能力**：
  - 智能体（Agent）应用：支持角色设定、多轮对话、工具调用（隐含于 RAG 流程中）；
  - RAG 增强：通过知识库实现私域问答，支持 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.png`, `.jpg` 等格式（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；
  - 多端嵌入：提供标准化 Web 悬浮挂件（文档 2）、企业微信/钉钉/公众号消息回调集成（文档 1、3、4）；
  - 本地 RAG 可选：支持完全本地部署的检索环节 + 云端大模型生成，适用于对数据主权或文档切分灵活性要求高的场景（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

> **注意**：文档 1 与文档 2 在模型选型建议上存在不一致——文档 1 推荐 `千问-Plus`，文档 2 明确使用 `Qwen3.5-Plus` 并说明其“能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间”。实际开发中应以控制台最新模型列表为准，`Qwen3.5-Plus` 是当前推荐的通用型模型。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **模型配置** | `temperature` | 控制输出随机性，值越高越发散（文档 5） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `max_tokens` | 限制生成回复最大 token 数（文档 5） | 同上 |
| | `history_rounds` | 控制参考历史对话轮数（文档 5） | 同上 |
| **RAG 配置** | `top_k`（召回片段数） | 检索时返回最相关文本片段数量（文档 5） | 同上 |
| | `similarity_threshold` | 过滤低于该相似度的检索结果（文档 5；文档 1/2/4 中对应“相似度阈值”） | 同上；[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| | `chunking_strategy` | 文档切分策略，影响检索精度（文档 5 明确提及可定制；文档 1/2/4 中为“文件处理”选项） | 同上；[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| **连接流配置** | `WebhookUrl` | AppFlow 生成的 HTTP 回调地址，用于接收企业微信/钉钉/公众号消息（文档 1、3、4） | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择模型、配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），发布应用并记录 `AppID` 和 `API Key`。
2. **准备知识库（可选但推荐）**：
   - 上传文件至百炼数据中心（文档 1/2/3/4）或本地 `File/` 目录（文档 5）；
   - 创建知识库，选择向量存储（云端推荐 ADB-PG；本地则直接存于 `VectorStore/`）；
   - 在应用配置中启用知识库，设置调用方式（如“必定调用”）和相似度阈值。
3. **配置目标平台连接流**：
   - **企业微信/钉钉/公众号**：使用 AppFlow 预置模板，配置平台凭证（企业 ID/AgentId/Secret 或 AppID/ClientID）和百炼凭证（API Key + AppID），获取 `WebhookUrl` 并在对应平台后台完成消息接收配置（文档 1、3、4）；
   - **网站嵌入**：在 AppFlow → 模型服务 AI 助手 → 创建 AI 助手 → Web 页面集成，获取悬浮挂件脚本，插入网站 HTML（文档 2）；
   - **本地 RAG**：解压 `local_rag.zip`，安装依赖，配置 API Key 环境变量，运行 `uvicorn main:app --port 7866` 启动 Web UI（文档 5）。
4. **验证与日志**：在目标平台发起对话测试；如需分析，可在 AppFlow 连接流中添加 SLS 日志节点（文档 1/3/4 均提供相同操作指引）。

## 限制和注意事项

- **免费额度**：新用户免费额度可覆盖教程消耗，但文档 2 特别注明 AppFlow、函数计算 FC 及 ADB-PG 向量存储为单独计费项（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
- **平台限制**：
  - 微信公众号未认证时，被动回复超时限制为 5 秒，易导致回复失败；强烈建议完成认证（文档 3）；
  - 钉钉机器人必须配置为 **HTTP 模式**，Stream 模式不兼容 AppFlow（文档 4）；
  - 企业微信配置需解决“域名主体校验未通过”问题，通常需配置自有备案域名或使用 AppFlow 内网代理（文档 1）。
- **技术限制**：
  - 百炼知识库单文件上限 100MB 或 1000 页，图片单张上限 20MB（文档 1）；
  - 本地 RAG 方案中，Embedding 模型 API 有流控，不建议上传 >100MB 文件（文档 5）；
  - 所有方案均要求百炼应用与 API Key 处于**同一业务空间**，否则鉴权失败（文档 2 常见问题明确指出）。
- **调试要点**：若出现 `request error` 或无响应，优先检查三项：API Key 状态、应用 ID 是否正确、百炼应用与 API Key 是否同属一个业务空间（文档 2）。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


