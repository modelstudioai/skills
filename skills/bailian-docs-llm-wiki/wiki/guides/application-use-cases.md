# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流渠道的 AI 助手/机器人快速集成，覆盖网站、企业微信、微信公众号、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现。开发者无需自行部署模型或构建推理服务，可复用百炼提供的模型能力、知识库管理与 API 接入能力，在 10 分钟内完成端到端上线。

## 支持的模型/功能

- **核心模型**：所有用例默认推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定），该模型在效果、速度与成本间取得平衡；文档 2、3、4 中则统一表述为“千问-Plus”，需注意二者为同一模型的不同命名方式。> **注意**：文档 5 中列出的 `qwen-max`、`qwen-plus`、`qwen3.5-flash` 均为当前可用商业模型，但 `qwen-plus` 与 `Qwen3.5-Plus` 实际指向同一模型版本，命名差异属历史兼容性问题，建议以控制台实际模型列表为准。
- **RAG 能力**：全部用例均依赖百炼知识库（Knowledge Base）实现私有知识增强，支持 PDF/DOCX/TXT/MD/PPTX/XLSX 等格式上传（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）、图像及结构化数据（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **交互载体**：支持 Web 悬浮窗（文档 1）、企业微信应用（文档 2）、微信公众号消息（文档 3）、钉钉机器人（文档 4）四类标准渠道；文档 5 提供本地 Gradio Web UI，适用于开发测试与私有化部署场景。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `AppID` / `应用ID` | 百炼应用唯一标识，用于调用模型 API，必须与 API Key 同属一个业务空间 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `API Key` | 百炼平台鉴权凭证，用于 AppFlow 或自定义后端调用模型服务 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| `AgentKey`（业务空间标识） | 用于校验 AppID 与 API Key 的归属一致性，不匹配将导致 `request error` | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `WebhookUrl` | AppFlow 连接流对外暴露的 HTTP 回调地址，需配置到企业微信/公众号/钉钉后台 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| `Token` & `EncodingAESKey` | 企业微信消息加解密必需参数，由 AppFlow 在创建企业微信凭证时生成 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`）并发布；
2. **配置知识库（可选但推荐）**：上传私有文档 → 创建知识库 → 在应用配置中启用「必定调用」并绑定知识库；
3. **创建渠道连接流**：
   - 网站：使用 AppFlow 创建「模型服务AI助手」，配置 Web 集成并嵌入悬浮挂件脚本；
   - 企业微信/公众号/钉钉：使用 AppFlow 预置模板（如 `企业微信自建应用大模型自动回复`），按向导完成三方凭证（企业 ID/AgentId/Secret 或 AppID/Client ID）与百炼凭证（API Key + AppID）绑定；
4. **渠道侧配置**：
   - 网站：在 HTML 中插入 AppFlow 生成的 `<script>` 标签；
   - 企业微信：在应用后台配置「API 接收消息」URL（即 WebhookUrl）及 Token/EncodingAESKey，并添加可信 IP；
   - 微信公众号：在后台开启「服务器配置」，填写 WebhookUrl 及 Token/EncodingAESKey（认证号支持全事件，未认证号仅限 5 秒被动回复）；
   - 钉钉：在应用配置中启用「HTTP 模式」机器人，设置 WebhookUrl（**严禁选择 Stream 模式**）；
5. **验证与日志**：通过渠道端发起对话；如需分析，可在 AppFlow 连接流中追加 SLS 日志节点记录原始请求与响应。

## 限制和注意事项

- **免费额度适用性**：新用户免费额度可覆盖全部文档所述场景的模型调用消耗（文档 1、2、3、4 均明确提及），但 AppFlow、函数计算 FC、ADB-PG 向量存储等配套云产品单独计费；
- **认证依赖**：微信公众号未认证时，消息响应超 5 秒即失败，必须使用「未认证公众号」专用模板（文档 3），或升级为认证号；
- **安全校验强制项**：
  - 企业微信要求域名主体备案与企业主体一致，否则需通过 AppFlow 部署 Nginx 代理或计算巢实例解决（文档 2）；
  - 企业微信可信 IP 仅允许单企业独占，多企业共用同一 IP 将触发安全拦截（文档 2）；
- **模型响应时效**：钉钉机器人要求 HTTP 模式下必须在 3 秒内返回响应，若百炼应用响应慢，需优化 Prompt（如添加“请简短回答”）、切换至 `qwen3.5-flash` 模型或调整知识库召回策略；
- **本地 RAG 差异**：文档 5 描述的本地部署方案（`local_rag`）完全独立于百炼控制台，其知识库、嵌入模型、切分逻辑均在本地运行，仅生成环节调用百炼 API，不适用于生产级高并发场景，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


