# application [use cases](use-cases.md)

百炼平台支持将大模型应用快速集成到多种终端渠道，包括网站、微信公众号、企业微信和钉钉，同时支持基于本地知识库构建 RAG 应用。开发者可以通过百炼创建智能体应用，结合 AppFlow 无代码连接器将应用部署到目标平台，实现 7x24 小时的 AI 智能客服或问答机器人。所有场景均支持通过知识库增强（RAG）来提升回答的专业性和准确性。

## 支持的集成渠道

百炼应用目前支持以下渠道的快速集成：

| 渠道 | 集成方式 | 核心依赖 |
|------|----------|----------|
| 网站 | AppFlow AI 助手 + 悬浮挂件脚本 | AppFlow Web 页面集成 |
| 微信公众号 | AppFlow 连接流模板 | 微信公众号后台 + AppFlow |
| 企业微信 | AppFlow 连接流模板 | 企业微信开发者中心 + AppFlow |
| 钉钉 | AppFlow 连接流模板 | 钉钉开放平台 + AppFlow |
| 本地 RAG | Python + LlamaIndex + Gradio | 本地环境 + 百炼 API |

各渠道的详细接入步骤可参考对应的原始文档：[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)、[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。

## 通用流程

无论目标渠道是什么，集成流程都遵循相似的步骤：

1. **创建百炼应用**：在百炼控制台创建智能体应用，选择合适的模型（如 Qwen3.5-Plus、千问-Plus 等），配置 Prompt 设定角色，发布应用。
2. **获取凭证**：在应用管理页面获取应用 ID，在密钥管理页面创建并保存 API Key。
3. **配置连接**：通过 AppFlow 创建连接流，将百炼应用与目标渠道关联（网站渠道则通过 AI 助手 + 悬浮挂件部署脚本嵌入）。
4. **验证效果**：在目标渠道发送消息，确认 AI 助手能正常响应。
5. **增加私有知识**（可选）：上传业务文档到百炼知识库，在应用中引用知识库并设置为"必定调用"，使 AI 能准确回答专业领域问题。

## 知识库配置（RAG）

知识库是提升 AI 回答专业性的关键。配置步骤如下：

1. **上传文件**：在百炼控制台的数据连接页面，通过默认文件连接器导入业务文档（支持 pdf、doc、docx、txt、md 等格式，单文档最大 100MB 或 1000 页）。
2. **创建知识库**：进入知识库页面，创建标准版知识库，选择已上传的文档。向量存储类型可选择默认或 ADB-PG（适合集中管理多应用向量数据）。
3. **关联应用**：在应用配置中添加知识库，调用方式设置为"必定调用"，测试验证后发布。

## 本地 RAG 应用

如果需要将知识库部署在本地以实现灵活的文档切分和嵌入模型选择，可参考 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 搭建本地 RAG 应用。该方案的特点：

- **检索在本地执行**：支持自定义切分策略、本地嵌入模型（如 GTE 系列），避免大文件上传问题。
- **生成调用云端 API**：使用百炼通义千问 API（qwen-max / qwen-plus / qwen-turbo），无需本地 GPU。
- **可调参数**：模型温度、最大回复长度、召回片段数、相似度阈值等。
- **环境要求**：Python 3.8 - 3.12，通过 `pip install -r requirements.txt` 安装依赖。

## 微信公众号的特殊注意事项

微信公众号集成时需注意认证状态的影响：

- **已认证公众号**：可使用客户消息接口回复用户，无响应时间限制。
- **未认证公众号**：只能使用被动回复消息功能，消息响应时间限制为 5 秒，超时将无法回复。可通过在 Prompt 中添加"请总是给出简短的回答"或选择千问-Turbo 模型来提升响应速度，但会降低回答效果。

> **注意**：微信公众号开启服务器配置后，之前配置的自定义菜单会因冲突被关闭。已认证的公众号可通过微信接口重新配置菜单，未认证公众号无法同时使用两项功能。详见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

## 企业微信的特殊注意事项

企业微信集成时可能遇到以下问题：

- **域名主体校验**：配置 API 接收消息时，若域名备案主体与企业主体不一致会校验失败，需要配置企业自有域名或使用计算巢 Nginx 代理。
- **企业可信 IP**：一个可信 IP 仅能用于一个企业，复用会被认定为服务商导致接口不可用。可使用阿里云 ECS 或托管实例进行请求转发。

## 上线建议

- 正式上线前建议组织业务人员参与应用评测，确保回答效果符合预期。
- 可通过优化提示词、完善知识库文档、调整文档切分策略等方法持续改进效果。
- 所有渠道均支持通过 AppFlow 添加 SLS 日志节点来记录对话日志，便于后续分析和优化。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)




