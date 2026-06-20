# application [use cases](use-cases.md)

百炼平台提供了多种将大模型应用集成到实际业务场景的方案，涵盖网站 AI 助手、微信公众号智能客服、企业微信 AI 助手、钉钉 AI 机器人以及本地知识库 RAG 应用。这些方案均以百炼智能体应用为核心，通过 AppFlow 等连接器实现零代码或低代码的快速集成。开发者可根据业务渠道选择合适的集成方式，并通过配置知识库实现私域知识问答。

## 通用流程

无论选择哪种集成渠道，核心流程大致相同：

1. **创建百炼智能体应用** -- 在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中创建智能体应用，选择合适的模型（如 Qwen3.5-Plus、千问-Plus 等），设置 Prompt 定义角色。
2. **获取 API 凭证** -- 在应用管理中获取应用 ID，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)中创建 API Key。
3. **通过连接器集成到目标渠道** -- 使用 AppFlow 或代码方式将应用接入网站、微信、钉钉等平台。
4. **配置知识库（RAG）** -- 上传私域文档、创建知识库并关联到应用，使 AI 能准确回答专业问题。

## 各渠道集成方案

### 网站 AI 助手

通过 AppFlow 的 AI 助手功能，可以在网站中嵌入一个可自定义的悬浮挂件。具体步骤包括创建百炼应用、在 AppFlow 中创建 AI 助手并导入模型、配置 Web 页面集成，最后将悬浮挂件部署脚本嵌入到网站 HTML 中。详细操作参见[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。

### 微信公众号智能客服

通过 AppFlow 提供的预置模板，可以将百炼应用与微信公众号连接。已认证的公众号支持客户消息回复（无时间限制），未认证的公众号只能使用被动回复消息功能（5 秒超时限制）。集成时需要在 AppFlow 中创建连接流，配置微信公众号凭证和百炼 API Key。详细操作参见[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

> **注意**：未认证的微信公众号受 5 秒响应限制，如果百炼应用回答超时将无法成功回复。可通过在 Prompt 中要求简短回答或选择千问-Turbo 模型来缓解，但会降低回答质量。

### 企业微信 AI 助手

通过 AppFlow 模板将百炼应用与企业微信自建应用对接，需要创建企业微信应用并获取企业 ID、AgentId、Secret，然后在 AppFlow 中配置连接流。额外需要配置 API 接收消息（填入 WebhookUrl、Token、EncodingAESKey）和企业可信 IP。详细操作参见[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

> **注意**：企业微信在配置 API 接收消息时可能遇到域名主体校验问题，需要配置企业自有域名或通过 Nginx 代理解决。配置企业可信 IP 时，若 IP 被识别为第三方服务商，需使用自有 ECS 或托管实例进行请求转发。

### 钉钉 AI 机器人

通过 AppFlow 模板将百炼应用与钉钉应用的机器人功能对接。需要在[钉钉开放平台](https://open-dev.dingtalk.com/)创建应用，获取 Client ID 和 Client Secret，并授予 `Card.Streaming.Write` 和 `Card.Instance.Write` 权限。机器人配置中消息接收模式必须选择 HTTP 模式。详细操作参见[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。

### 本地知识库 RAG 应用

如果需要将知识库部署在本地而非云端，可以使用百炼提供的示例应用，基于 LlamaIndex + Gradio 构建本地 RAG 系统。本地检索 + 云端通义千问 API 生成的架构兼顾了数据安全和推理质量。支持临时文件上传和持久化知识库两种模式。详细操作参见[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 知识库配置要点

各方案中配置知识库的流程基本一致：

1. **上传文件** -- 通过百炼控制台的数据连接或文件管理上传私域文档（支持 PDF、DOCX、TXT、XLSX 等格式，单文档最大 100MB 或 1000 页）。
2. **创建知识库** -- 在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建标准版知识库，选择已上传的文档。向量存储类型可选 ADB-PG 以集中管理多个应用的向量数据。
3. **关联应用** -- 在应用配置中添加知识库，调用方式设为"必定调用"，测试验证后发布。

## 模型选择建议

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| Qwen3.5-Plus / 千问-Plus | 效果、速度、成本均衡 | 通用客服场景（推荐） |
| 千问-Max | 性能最优 | 对回答质量要求高的场景 |
| 千问-Turbo | 速度快、价格低 | 对响应时间敏感的场景（如未认证微信公众号） |

## 对话日志记录

各渠道均可通过在 AppFlow 连接流中添加 SLS 日志节点来记录 AI 对话日志。需要在阿里云日志服务中创建 Project 和 Logstore，开启索引后即可进行在线日志查询和分析。

## 上线前建议

- 组织业务人员参与[应用评测](https://help.aliyun.com/zh/model-studio/evaluate-application/)，确保回答效果符合预期
- 通过优化提示词、完善私有知识、调整文档切分策略等方法持续改进回答质量

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


