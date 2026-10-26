# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置知识库 → 在目标渠道通过 AppFlow 建立连接流 → 发布并验证。开发者可复用同一套知识库与提示词策略，降低多端维护成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档 3 提及用于提速）。
- **RAG 能力**：所有用例均依赖百炼知识库功能实现私域知识增强，支持 PDF/DOCX/TXT/CSV/XLSX 等格式上传（[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)、[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)、[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）。
- **本地 RAG 变体**：文档 5 提供了完全本地化部署方案，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及灵活参数调优，适用于对数据主权或定制化有强需求的场景。

> **注意**：文档 1、2、3、4 中均将模型简称为“千问-Plus”，但文档 1 明确使用 `Qwen3.5-Plus`，而其他文档未注明版本号。实际配置时请以百炼控制台当前可用模型列表为准，避免因模型下线导致调用失败。

## 关键参数

| 参数 | 说明 | 典型值 | 来源 |
|------|------|--------|------|
| `applicationId` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | `app-xxxxxx` | 所有文档共用 |
| `API Key` | 百炼 API 认证密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | `sk-xxxxxxxx` | 所有文档共用 |
| `AgentKey`（业务空间标识） | 用于鉴权，必须与 API Key 所属业务空间一致 | `space-xxxxxx` | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中强调此项 |
| `WebhookUrl` | AppFlow 连接流生成的回调地址，需填入各渠道后台（企业微信/公众号/钉钉） | `https://xxx.appflow.aliyuncs.com/...` | 文档 2、3、4 共用 |
| `Token` & `EncodingAESKey` | 企业微信消息加解密必需参数，由 AppFlow 凭证配置页生成 | 自动生成字符串 | 文档 2 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（推荐 `Qwen3.5-Plus`）→ 设置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）→ 发布。
2. **配置知识库**：
   - 上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件中心](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)；
   - 进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建标准版知识库；
   - 在应用配置中启用知识库，设置调用方式为 `必定调用`。
3. **配置渠道连接流**：
   - **网站**：AppFlow → 模型服务AI助手 → 创建AI助手 → 导入百炼模型 → Web页面集成 → 获取悬浮挂件脚本 → 插入 HTML。
   - **企业微信/公众号/钉钉**：AppFlow → 使用对应预置模板（如 `企业微信自建应用大模型自动回复`）→ 授权渠道凭证（企业ID/AgentId/Secret 或 AppID/AppSecret）→ 绑定百炼 API Key 与 applicationId → 获取 WebhookUrl → 填入渠道后台（企业微信 API接收消息 / 公众号服务器配置 / 钉钉机器人 HTTP模式地址）。
4. **验证与日志**：对话测试后，可通过 AppFlow 运行日志排查失败步骤；如需长期分析，可在连接流中添加 SLS 日志节点记录对话（文档 2、3、4 均提供详细步骤）。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **认证要求**：
  - 微信公众号：未认证账号仅支持被动回复（5秒超时限制），建议完成认证以启用客户消息接口（文档 3）；
  - 企业微信/钉钉：需确保管理员账号完成开放平台授权，且应用已开通必要权限（如企业微信的 `接收消息`、钉钉的 `Card.Streaming.Write`）。
- **安全限制**：
  - 企业微信要求配置可信 IP（文档 2），若使用 AppFlow 默认出口 IP 不满足要求，需启用内网代理或 Nginx 转发；
  - 微信公众号配置服务器时若报“URL存在严重安全风险”，需改用服务商授权模式（文档 3）；
  - 钉钉机器人**必须**选择 HTTP 模式，Stream 模式不兼容（文档 4）。
- **性能边界**：
  - 知识库单文档上限 100MB 或 1000 页（文档 2）；
  - 本地 RAG 方案中，Embedding API 限流可能导致大文件创建知识库耗时过长（文档 5）；
  - “Failed to stream content” 错误通常源于前端请求地址未替换为真实 WebhookUrl（文档 1）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


