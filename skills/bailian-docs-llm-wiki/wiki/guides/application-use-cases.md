# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手/机器人快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的百炼大模型应用与知识库能力，通过 AppFlow 低代码编排实现渠道对接，无需自行维护推理服务或向量检索基础设施。核心模式为“云端模型 + 可选本地/云端知识库 + 渠道适配层”，适用于客户支持、私域运营、内部提效等典型 RAG 应用。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（即文档中所述 `Qwen3.5-Plus`），在效果、速度与成本间取得平衡；亦支持 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）及 `qwen-turbo`（极致响应速度）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **知识增强（RAG）**：支持通过百炼知识库或本地知识库（如 `local_rag` 示例）接入私有文档，实现结构化/非结构化数据问答 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **多渠道适配**：提供开箱即用的 AppFlow 模板，覆盖网站悬浮助手、微信公众号智能客服、企业微信自建应用、钉钉群机器人四类主流入口 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

> **注意**：文档 1 与文档 2–5 在模型名称表述上存在不一致——文档 1 明确使用 `Qwen3.5-Plus`，而文档 2、4、5 统一称为 `千问-Plus`，文档 3 则列为 `qwen-plus`。三者实为同一模型，建议以控制台实际可选模型 ID（如 `qwen-plus`）为准，避免依赖版本别名。

## 关键参数

| 参数 | 说明 | 取值建议 |
|--------|------|-----------|
| **模型温度（temperature）** | 控制生成随机性 | 生产环境建议设为 `0.1–0.5`，降低幻觉风险 |
| **最大输出长度（max_tokens）** | 限制回复 token 数 | 网页/公众号等轻交互场景建议 `512`；长文档摘要可设 `2048` |
| **召回片段数（top_k）** | RAG 检索返回的最相关段落数 | 默认 `3`；知识密度高时可降至 `1–2`，避免噪声干扰 |
| **相似度阈值（similarity_threshold）** | 过滤低相关性检索结果 | 范围 `0.0–1.0`，`0.6–0.75` 为常用安全区间 |
| **携带上下文轮数（history_rounds）** | 模型可见的历史对话轮次 | 单轮问答设 `0`；需多轮推理设 `3–5` |

## 使用方式

1. **创建百炼应用**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中创建「智能体应用」，配置 Prompt（如角色设定）与模型（如 `qwen-plus`），发布后获取 `应用ID` 与 `API Key`。
2. **准备知识源**：
   - *云端知识库*：上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)，在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)中创建并绑定至应用；
   - *本地知识库*：使用 `local_rag` 示例工程，在本地切分文档、选择嵌入模型（支持百炼 API 或 ModelScope 本地模型），通过 Gradio UI 或 API 调用 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
3. **配置渠道连接流**：
   - 访问 AppFlow 控制台，选用对应渠道模板（如[企业微信自建应用大模型自动回复](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-qiyeweixinself0813shzoa?from=solution)）；
   - 分步配置渠道凭证（如企业微信 `AgentId/Secret`、钉钉 `Client ID/Secret`、公众号 `AppID`）与百炼凭证（`API Key` + `应用ID`）；
   - 发布后获取 `WebhookUrl` 并按渠道要求完成回调地址配置（如企业微信的 API 接收消息、钉钉机器人的 HTTP 模式地址）。

## 限制和注意事项

- **免费额度范围**：新用户免费额度可覆盖全部入门教程消耗，但仅限百炼模型调用；AppFlow、函数计算（FC）、ADB-PG 向量库等依赖云产品单独计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **渠道能力差异**：
  - 微信公众号未认证时，仅支持被动回复（5 秒超时限制），必须启用 `qwen-turbo` 或精简 Prompt 保响应 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；
  - 钉钉机器人**必须**使用 HTTP 模式，Stream 模式不兼容 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)；
  - 企业微信需配置可信 IP，若使用第三方代理（如 ECS/Nginx），须通过 AppFlow 内网代理功能授权并添加白名单 IP。
- **知识库文件限制**：百炼云端知识库单文件上限 100MB 或 1000 页；`local_rag` 工程受限于 Embedding API 限流，不建议单次上传 >100MB 文件。
- **调试与日志**：所有渠道均可在 AppFlow 中添加 SLS 日志节点记录完整对话链路，用于效果分析与问题定位 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)


