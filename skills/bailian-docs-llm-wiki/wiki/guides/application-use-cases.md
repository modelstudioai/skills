# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将大模型问答能力嵌入网站、微信公众号、企业微信、钉钉等主流渠道，无需从零开发后端服务或部署模型。所有方案均基于百炼应用（智能体）作为推理核心，通过 AppFlow 实现与各平台的消息协议对接，并支持通过知识库注入业务私域数据以提升回答准确性。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中统一表述），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务。  
- **RAG 增强**：所有用例均依赖百炼知识库功能实现私有知识注入，支持 PDF/DOCX/TXT/Excel 等格式上传，自动解析并构建向量索引；知识调用方式支持“必定调用”等策略 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **本地 RAG 变体**：文档 5 提供了完全本地化部署的 RAG 方案，支持自定义文档切分、本地 embedding 模型（如 GTE-Chinese-Large）、以及 qwen-max/qwen-plus/qwen-turbo 多模型切换，适用于对数据主权和定制性要求更高的场景 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
> **注意**：文档 1 使用 `Qwen3.5-Plus`，而文档 2–4 统一使用 `千问-Plus`。二者为同一模型的不同命名版本，实际能力一致，但建议在生产环境中以控制台最新模型列表为准，避免因版本别名导致配置偏差。

## 关键参数

| 参数 | 说明 | 来源位置 |
|------|------|----------|
| `App ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取，必须与 API Key 同属一个业务空间 | 所有文档 1–4 的“1.2 获取调用 API 所需的应用ID和API Key”节 |
| `API Key` | 百炼服务调用凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建，用于 AppFlow 或本地应用鉴权 | 所有文档 1–4 的“1.2 获取调用 API 所需的应用ID和API Key”节 |
| `AgentKey`（业务空间标识） | 用于校验 API Key 与智能体归属一致性，若不匹配将导致 `request error` | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题节 |
| `WebhookUrl` | AppFlow 生成的 HTTP 回调地址，需填入企业微信/钉钉/微信公众号后台，作为消息接收入口 | 文档 3、4、2 的连接流发布后步骤中强调复制保存 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建**智能体应用** → 选择 `Qwen3.5-Plus` 或 `千问-Plus` → 配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）→ 发布。  
2. **准备私有知识**（可选但推荐）：上传业务文档至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) → 创建知识库 → 在应用配置中启用并设置调用方式为“必定调用”。  
3. **选择集成渠道并配置 AppFlow**：  
   - **网站嵌入**：使用 AppFlow 创建 AI 助手 → 配置悬浮挂件 → 将生成的 JS 脚本插入 HTML `<head>` 或 `<body>` 底部 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
   - **微信公众号**：根据认证状态选择对应模板（已认证/未认证）→ 授权公众号 → 绑定百炼应用 → 发布连接流。  
   - **企业微信/钉钉**：创建对应平台应用 → 获取平台凭证（CorpID/AgentId/Secret 或 ClientID/ClientSecret）→ 在 AppFlow 中配置双凭证（平台 + 百炼）→ 填写 WebhookUrl 并完成平台侧配置（可信 IP、API 接收等）。  
4. **本地 RAG（进阶）**：下载 `local_rag.zip` → 安装依赖（Python 3.9–3.12）→ 配置环境变量 `BAI_LIAN_API_KEY` → 运行 `uvicorn main:app --port 7866` → 通过 Gradio 界面上传文件、创建知识库、调整 RAG 参数。

## 限制和注意事项

- **免费额度适用性**：新用户免费额度覆盖百炼模型调用，但 AppFlow、函数计算 FC、ADB-PG 向量存储等依赖云产品单独计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。  
- **微信公众号响应时限**：未认证公众号受 5 秒响应限制，超时即失败；建议完成认证或改用 `千问-Turbo` 模型提速 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 常见问题节。  
- **企业微信/钉钉域名与 IP 校验**：API 接收 URL 需通过主体备案校验；若无自有域名，必须启用 AppFlow 内网代理（Nginx/ECS 托管）并配置可信 IP，否则无法通过验证 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 常见问题节。  
- **文件上传限制**：云端知识库单文件 ≤ 100MB 或 1000 页；本地 RAG 方案同样不建议上传 >100MB 文件，以防 embedding 超时 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。  
- **调试与日志**：所有 AppFlow 连接流均支持添加 SLS 日志节点记录对话，便于效果分析与问题排查，详见各文档“记录 AI 助理对话日志”小节。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


