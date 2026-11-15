# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 无代码连接流实现端到端交付，开发者只需配置模型、知识库与渠道凭证，无需编写后端逻辑。核心能力包括私有知识注入、多轮对话管理、Webhook 自动路由及日志可追溯性。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（即文档中多次提及的“千问-Plus”），兼顾效果、速度与成本；亦支持 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）及 `qwen3.5-plus`（文档 1 中明确指定）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 增强**：所有渠道均支持知识库引用，知识源可为 PDF/DOCX/TXT/CSV 等格式，支持全文引用、切片检索或自定义处理三种模式（文档 2、3、5 统一描述）。
- **本地化部署选项**：除云端 RAG 外，还提供基于本地知识库的完整 RAG 应用方案，支持自定义文档切分、嵌入模型替换（如 GTE-Chinese-Large）及本地向量存储 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **交互扩展能力**：支持卡片消息（钉钉）、富文本回复（企业微信）、悬浮挂件（网站）、被动/主动消息（微信公众号）等多种交互形态。

> **注意**：文档 1 明确要求模型为 `Qwen3.5-Plus`，而文档 2、3、5 均写为 `千问-Plus`（即 `qwen-plus`）。二者为不同模型版本，`Qwen3.5-Plus` 是更新迭代版本，性能更优。实际部署时应以控制台最新可用模型为准，避免硬编码旧模型名。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可选值/约束 |
|----------|--------|------|-------------|
| **模型参数** | `temperature` | 控制输出随机性 | 0.0–1.0，默认 0.7 |
| | `max_tokens` | 最大生成 token 数 | ≥1，建议 512–2048 |
| | `top_p` | 核采样阈值 | 0.0–1.0，默认 0.95 |
| **RAG 参数** | `retrieval_top_k` | 检索召回片段数 | 1–10，默认 3 |
| | `similarity_threshold` | 相似度过滤阈值 | 0.0–1.0，默认 0.3（文档 2、5 中隐含使用） |
| | `knowledge_call_mode` | 知识调用方式 | `always`（必定调用）、`on_demand`（按需）、`never`（不调用） |
| **渠道参数** | `webhook_url` | AppFlow 生成的回调地址 | 必须在对应平台（微信/企微/钉钉）完成白名单与 Token 配置 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼应用**：在百炼控制台 → 应用管理 → 创建智能体应用，选择模型、配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），发布前务必测试。
2. **获取凭证**：记录应用 ID 与 API Key（均在百炼控制台对应页面获取）。
3. **配置渠道连接流**：
   - 网站：使用 AppFlow → 模型服务 AI 助手 → Web 页面集成，嵌入悬浮挂件脚本；
   - 微信公众号/企业微信/钉钉：使用 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`），按向导完成三方凭证（AppID/Secret/ClientID 等）与百炼凭证绑定；
4. **接入私有知识**：上传文件至百炼数据连接 → 创建知识库 → 在应用配置中启用并关联知识库 → 发布；
5. **验证与上线**：在目标渠道发起对话，检查响应内容、引用来源及延迟；正式上线前建议执行人工评测 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。

## 限制和注意事项

- **免费额度限制**：新用户享有百炼 API 调用免费额度，覆盖教程全部消耗；额度耗尽后按 token 计费；AppFlow、FC、ADB-PG 等依赖云产品单独计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **渠道认证要求**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口；
  - 企业微信/钉钉需确保应用已获相应权限（如 `Card.Streaming.Write`、通讯录读取等），否则 Webhook 调用将失败；
- **安全配置强制项**：
  - 企业微信需配置可信 IP 白名单（AppFlow 提供 IP 列表）；
  - 微信公众号配置服务器 URL 时若报“安全风险”，需改用服务商授权或 Nginx 代理方案；
- **本地 RAG 注意事项**：Python 版本需为 3.9–3.12；Embedding 模型 API 有流控，单文件不宜超过 100 MB；Windows 用户需额外安装 `msvc-runtime` [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **调试建议**：遇到 `Failed to stream content` 或无响应时，优先检查浏览器控制台网络请求、AppFlow 运行日志及凭证是否跨业务空间（文档 1 常见问题章节明确指出该鉴权错误）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


