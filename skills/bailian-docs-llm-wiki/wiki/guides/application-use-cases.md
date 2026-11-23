# application [use cases](use-cases.md)

百炼平台支持将大模型能力快速集成到主流企业通讯与业务平台中，实现开箱即用的 AI 助手、智能客服或机器人。典型场景包括在企业微信、钉钉、微信公众号和网站嵌入 RAG 增强型问答应用，所有方案均基于 AppFlow 低代码连接流实现端到端对接，无需自行开发后端服务。核心能力依赖百炼托管的模型 API、知识库（RAG）与统一凭证体系，开发者只需关注应用配置、知识注入与渠道适配。

## 支持的模型/功能

- **基础模型**：支持 `qwen-plus`（文档 1、3、4 中默认推荐）、`qwen3.5-plus`（文档 2 明确指定）、`qwen-max` 和 `qwen3.5-flash`（文档 5 列出可选模型）。> **注意**：文档 1 与文档 2 对默认模型选择不一致（前者为 `qwen-plus`，后者为 `qwen3.5-plus`），实际部署时请根据延迟/效果权衡选择，并以控制台最新可用模型列表为准。
- **RAG 能力**：所有用例均依赖知识库检索增强，支持上传 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式文件（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；本地 RAG 方案还支持结构化/非结构化数据分离管理（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **交互形式**：支持群聊/私聊消息回复（企业微信、钉钉、微信公众号）、悬浮挂件（网站）、卡片消息（钉钉）、流式响应（全部）及 DeepSeek 思考过程展示（仅钉钉，见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）。

## 关键参数

| 参数 | 说明 | 来源位置 |
|------|------|----------|
| `AppId`（百炼应用 ID） | 百炼控制台「应用管理」页面获取，用于标识调用目标应用 | 所有文档 1–4 的「1.2 获取调用 API 所需的应用ID和API Key」章节 |
| `API Key` | 百炼控制台「API Key」页面创建，用于身份鉴权 | 所有文档 1–4 的「1.2 获取调用 API 所需的应用ID和API Key」章节 |
| `WebhookUrl` | AppFlow 连接流发布后生成，作为第三方平台（如企业微信、钉钉）的消息接收地址 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 的第 3 节、[在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 的第 3 节 |
| `Token` & `EncodingAESKey` | 仅企业微信必需，由 AppFlow 在配置企业微信凭证时生成，用于消息加解密 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 的第 3 节 |
| `召回片段数` / `相似度阈值` | 本地 RAG 方案中可调参数，直接影响检索质量 | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的「优化回复效果」章节 |

## 使用方式

1. **创建百炼应用**：在百炼控制台「应用管理」创建智能体应用，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），选择模型，发布应用。
2. **准备知识库（可选但推荐）**：上传业务文档至百炼「文件」或「数据连接」，在「知识库」页面创建并关联至应用；或使用本地 RAG 方案（文档 5）自主管理切分与嵌入。
3. **配置连接流**：
   - 企业微信：使用 AppFlow 预置模板，配置企业微信凭证（企业 ID、AgentId、Secret）与百炼凭证（API Key、AppId），获取 WebhookUrl 并填入企业微信后台「API 接收消息」。
   - 微信公众号：根据认证状态选择对应模板，通过扫码授权公众号，配置百炼凭证与 AppId。
   - 钉钉：创建钉钉应用获取 Client ID/Secret，在 AppFlow 中配置双凭证，将 WebhookUrl 填入钉钉机器人「HTTP 模式」接收地址。
   - 网站：在 AppFlow「模型服务 AI 助手」中创建助手，导入百炼模型，生成悬浮挂件脚本，插入网站 HTML。
4. **验证与日志**：通过对应渠道发起对话测试；如需分析，可在 AppFlow 连接流中追加 SLS 日志节点（所有文档均提及该能力）。

## 限制和注意事项

- **企业微信可信 IP 限制**：企业微信要求回调请求必须来自白名单 IP，若使用 AppFlow 直连可能触发“第三方服务商”报错。必须通过内网代理（ECS 或 Nginx）转发，并将代理机器公网 IP 加入企业微信「企业可信 IP」（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 的「常见问题」章节）。
- **微信公众号响应超时**：未认证公众号强制 5 秒内响应，超时即失败；建议完成认证或选用 `qwen-turbo` 等高速模型（文档 3「常见问题」）。
- **钉钉机器人模式限制**：仅支持 HTTP 模式，Stream 模式不可用（文档 4「4.1 配置钉钉机器人」强调）。
- **文件处理限制**：百炼云端知识库单文件 ≤100 MB 或 1000 页，图片 ≤20 MB，最多 200 个文件（文档 1）；本地 RAG 方案建议单文件 ≤100 MB（文档 5）。
- **免费额度覆盖范围**：新用户免费额度可覆盖百炼模型调用，但 AppFlow、函数计算 FC、ADB-PG 等关联云产品单独计费（文档 2 明确说明）。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


