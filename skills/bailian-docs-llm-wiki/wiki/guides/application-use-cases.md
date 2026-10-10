# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将智能问答能力嵌入网站、微信公众号、钉钉、企业微信等主流渠道，无需从零搭建后端服务或管理模型推理环境。所有方案均基于百炼托管的模型 API 和 AppFlow 可视化编排能力实现，适用于客服、内部支持、产品咨询等 7×24 小时响应场景。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 统一表述），该模型在效果、速度与成本间取得平衡，适用于通用问答任务；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）等变体 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 增强**：所有场景均支持通过百炼知识库模块接入私有文档（PDF/DOCX/TXT 等），启用“必定调用”模式确保关键问题必检索知识 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **多端集成能力**：提供开箱即用的 AppFlow 模板，覆盖 Web（悬浮挂件）、微信公众号（消息回复）、钉钉（机器人卡片）、企业微信（自建应用）四类渠道，均无需编写业务逻辑代码 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2–4 统一写作 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 是其新版命名），但控制台 UI 和 API 参数中应以百炼控制台实际下拉选项为准，避免硬编码模型 ID。

## 关键参数

| 参数 | 说明 | 来源位置 |
|------|------|----------|
| `app_id` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 所有文档 1–4 的“1.2 获取调用 API 所需的应用ID和API Key”节 |
| `api_key` | 百炼 API 访问密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建 | 所有文档 1–4 的“1.2 获取调用 API 所需的应用ID和API Key”节 |
| `AgentKey`（业务空间标识） | 用于鉴权校验，必须与 `api_key` 所属业务空间一致，否则触发 `request error` | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) “常见问题”节 |
| `WebhookUrl` | AppFlow 生成的 HTTP 回调地址，用于企业微信/钉钉接收消息 | 文档 3、4 的“创建连接流”步骤末尾 |
| `相似度阈值` / `召回片段数` | RAG 检索阶段核心参数，影响知识召回精度与噪声水平，可在知识库引用配置或本地 RAG 应用中调整 | [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) “优化回复效果”节 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建**智能体应用** → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt（例如 `"你叫小助，帮助解答产品选购问题"`）→ 发布。
2. **准备私有知识（可选但推荐）**：
   - 上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)；
   - 在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建标准版知识库；
   - 在应用配置页的“文档”区域添加知识库，调用方式设为**必定调用**。
3. **选择集成渠道并配置 AppFlow**：
   - **网站**：AppFlow → 模型服务AI助手 → 创建助手 → 导入百炼模型 → Web 页面集成 → 复制悬浮挂件脚本插入 HTML。
   - **微信公众号**：AppFlow → 使用预置模板 → 授权公众号凭证 → 配置百炼 `app_id`/`api_key` → 发布。
   - **钉钉/企业微信**：AppFlow → 使用对应模板 → 分别配置钉钉 `Client ID/Secret` 或企业微信 `AgentId/Secret/CorpID` → 获取 `WebhookUrl` → 在钉钉开放平台或企业微信后台完成机器人/API 接收配置。
4. **验证与日志（可选）**：可通过 AppFlow 添加 SLS 日志节点记录对话，便于后续分析 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 限制和注意事项

- **免费额度限制**：新用户可享百炼 API 免费调用额度，覆盖教程全部操作；额度耗尽后按 token 计费。AppFlow、函数计算 FC、ADB-PG 向量存储等依赖服务单独计费 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **微信认证约束**：未认证公众号仅支持被动回复（5 秒超时限制），建议完成微信认证以启用客户消息接口 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- **企业微信域名与 IP 安全要求**：API 接收 URL 需通过域名主体校验；可信 IP 必须为企业自有服务器 IP，第三方服务商 IP（如直接使用 AppFlow 默认 Webhook）会被拒绝，需配置 Nginx 代理或计算巢实例解决 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- **本地 RAG 差异**：文档 5 描述的 `build-rag-application-based-on-local-retrieval.md` 方案为全本地检索 + 云端生成架构，适用于需完全掌控切分逻辑与嵌入模型的场景，但不兼容 AppFlow 一键集成流程，属于独立部署路径。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


