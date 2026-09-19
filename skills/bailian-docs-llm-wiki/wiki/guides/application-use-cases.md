# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 多端集成”展开。开发者可基于百炼托管的大模型 API 快速构建智能客服、知识问答等应用，并通过 AppFlow 低代码连接微信公众号、企业微信、钉钉、网站等渠道，或通过本地部署方式实现对知识库和检索过程的完全控制。所有方案均默认支持 RAG 增强，且可复用统一的百炼应用配置与知识库资源。

## 支持的模型/功能

- **基础模型**：官方推荐 `qwen-plus`（效果、速度、成本均衡），也支持 `qwen-max`（高精度）、`qwen-turbo`（低延迟）及 `qwen3.5-plus`（文档 1 中明确指定）[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 能力**：所有集成方案均默认启用知识库检索增强，支持上传 PDF/DOCX/TXT/Excel 等格式文件（单文件 ≤100 MB），并提供“全文引用”、“切片检索”、“自定义处理”三种文档处理方式 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **部署模式**：
  - **云端全托管**：通过百炼控制台创建智能体应用 + AppFlow 连接流，适用于网站、企微、钉钉、公众号等标准渠道；
  - **本地混合部署**：支持将检索环节（切分、向量化）部署在本地，生成环节调用百炼 API，适用于对数据主权或切分策略有强定制需求的场景 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 明确要求模型选择 `Qwen3.5-Plus`，而文档 2、3、5 均写为 `千问-Plus`（即 `qwen-plus`）。二者为不同版本，`Qwen3.5-Plus` 是更新迭代后的商用模型，推荐以文档 1 的命名为准；若控制台未显示该选项，应使用 `qwen-plus` 作为兼容替代。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | 温度（temperature） | 控制输出随机性，值域 0–2，建议生产环境设为 0.1–0.5 | 本地 RAG 应用的 Gradio 界面或 `chat.py` 配置项 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | 最大回复长度（max_tokens） | 限制响应 token 数量，影响回答详略程度 | 同上 |
| | 携带上下文轮数 | 控制历史对话记忆深度，设为 1 表示不依赖上下文 | 同上 |
| **RAG 层** | 召回片段数（top_k） | 检索返回给模型的最相关文本段数量，默认 3–5 | 同上；云端应用在知识库引用配置中可设“相似度阈值”与“权重” |
| | 相似度阈值 | 过滤低相关性召回结果，值域 0–1，值越高越严格 | 百炼应用配置页 > 知识库 > 编辑知识项 |

## 使用方式

1. **创建百炼应用**：进入 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择“智能体应用”，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），发布应用；
2. **获取凭证**：在 [API Key](https://bailian.console.aliyun.com/?tab=app#/api-key) 页面创建 Key，在应用详情页复制 Application ID；
3. **配置知识库（可选但推荐）**：
   - 上传文件至 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 或 [文件中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)；
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 创建标准版知识库，关联文件；
   - 在应用配置中启用知识库，设置调用方式（如“必定调用”）；
4. **选择集成渠道并配置连接流**：
   - **网站**：使用 AppFlow 创建“模型服务AI助手”，配置 Web 集成，嵌入悬浮挂件脚本；
   - **企业微信/钉钉/公众号**：使用对应 AppFlow 模板（如 `tl-qiyeweixinself0813shzoa`），完成三方凭证授权与 Webhook 绑定；
   - **本地部署**：下载 `local_rag.zip`，配置 Python 环境与 API Key，运行 `uvicorn main:app --port 7866` 启动服务。

## 限制和注意事项

- **免费额度**：新用户可享百炼 API 免费调用额度，覆盖教程全部操作；额度耗尽后按 token 计费 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)；
- **文件限制**：云端知识库单文件 ≤100 MB 或 1000 页，图片 ≤20 MB，最多上传 200 个文件；本地 RAG 应用受限于 Embedding API 限流，不建议上传 >100 MB 文件 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；
- **认证依赖**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），认证后方可使用客户消息接口 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)；
  - 钉钉应用需管理员授予 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限，且机器人必须配置为 **HTTP 模式**（非 Stream 模式） [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)；
- **安全要求**：企业微信/钉钉/公众号均需配置可信 IP 白名单，AppFlow 会生成对应 IP 列表，需手动填入各平台后台；若无自有服务器，可使用 AppFlow 提供的 Nginx 代理实例 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；
- **调试建议**：上线前务必进行人工评测，利用 [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md) 工具验证回答准确性，再通过优化 Prompt、调整切分策略或更换 Embedding 模型持续改进。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


