# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 无代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置知识库 → 在目标渠道通过 AppFlow 绑定模型与消息入口。开发者可复用同一套知识库和提示词策略，降低多端维护成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；`qwen-max` 和 `qwen3.5-flash` 亦受支持，详见[本地 RAG 应用文档](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)中的参数说明。
- **RAG 能力**：所有集成方案均支持知识库增强，可上传 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式文件（文档 2 明确列出支持格式及单文件 100MB 限制）。
- **交互形式**：支持 Web 悬浮挂件（文档 1）、微信公众号被动/主动回复（文档 3）、企业微信自建应用（文档 2）、钉钉机器人卡片（文档 4），以及本地部署的 Gradio Web UI（文档 5）。

> **注意**：文档 1 中推荐 `Qwen3.5-Plus`，而文档 2、3、4 均写为“千问-Plus”。经核实，`Qwen3.5-Plus` 是当前最新命名，`千问-Plus` 为旧称，二者指向同一模型。建议以控制台实际可选模型名称为准，避免硬编码旧名。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `AppID` / `应用ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `API Key` | 百炼调用凭证，需在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| `AgentKey`（业务空间标识） | 用于校验 API Key 与智能体是否同属一个业务空间，排查 `request error` 的关键字段 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `WebhookUrl` | AppFlow 连接流对外暴露的 HTTP 入口地址，需配置到微信公众号、企业微信或钉钉后台 | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) |
| `Token` & `EncodingAESKey` | 企业微信消息加解密必需参数，由 AppFlow 在创建企业微信凭证时生成 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |

## 使用方式

1. **创建百炼智能体应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 设置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）→ 发布。
2. **配置知识库（可选但推荐）**：进入百炼控制台 → 数据连接 → 上传文件 → 知识库 → 创建标准版知识库 → 在应用配置中启用并关联知识库（调用方式建议设为 `必定调用`）。
3. **创建渠道连接流**：
   - **网站**：AppFlow → 模型服务 AI 助手 → 创建 AI 助手 → 导入百炼模型 → Web 页面集成 → 获取悬浮挂件脚本 → 插入 HTML。
   - **微信公众号/企业微信/钉钉**：AppFlow → 使用对应预置模板（如 `tl-qiyeweixinself0813shzoa`）→ 授权渠道账号 → 配置百炼凭证 → 填写应用 ID → 发布 → 将生成的 `WebhookUrl` 或 `Token` 等填入对应平台后台。
4. **验证与日志**：在目标渠道发起对话；如遇问题，通过 AppFlow 运行日志排查（文档 3 提供详细日志查看路径），或添加 SLS 日志节点记录全链路对话（文档 2、3、4 均提及该能力）。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **认证要求**：
  - 微信公众号：未认证账号仅支持 5 秒内被动回复，超时即失败；认证后支持主动消息与更长响应窗口（文档 3 强调此限制）。
  - 企业微信/钉钉：需确保应用已获取相应权限（如企业微信的 `接收消息` 权限、钉钉的 `Card.Streaming.Write` 权限），否则无法收发消息。
- **安全配置**：
  - 企业微信需配置可信 IP 白名单（文档 2 提供 ECS/Nginx 代理方案）；
  - 微信公众号配置服务器时若报“URL 存在严重安全风险”，需改用服务商授权模式（文档 3 提示）；
  - 所有渠道均需确保 `WebhookUrl` 可被公网访问且 HTTPS 有效（文档 2 的域名主体校验问题即源于此）。
- **本地 RAG 特殊性**：文档 5 描述的本地部署方案不依赖 AppFlow，需自行管理 Python 环境（3.9–3.12）、Embedding 模型（支持云端 API 或本地 ModelScope 模型），且知识库存储于本地 `VectorStore` 目录，适用于对数据主权有强要求的场景。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


