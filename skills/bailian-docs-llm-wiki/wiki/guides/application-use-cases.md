# application [use cases](use-cases.md)

百炼平台支持多种企业级 AI 应用场景，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可快速将智能问答能力嵌入网站、微信公众号、企业微信、钉钉等主流渠道，无需从零搭建模型服务或维护向量数据库。所有方案均基于百炼托管的模型 API 和 AppFlow 可视化编排能力实现，兼顾开发效率与生产稳定性。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中统一表述），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景。`qwen-max` 和 `qwen-turbo` 也受支持，分别适用于高精度与低延迟场景 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **RAG 增强**：所有渠道方案均支持通过百炼知识库接入私有文档（PDF/DOCX/TXT 等），实现领域知识精准召回。知识库支持标准版（默认）及 ADB-PG 向量存储选项，后者适用于多应用共享向量数据的集中管理场景 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **扩展能力**：支持自定义 Prompt 引导角色与回答风格（如“请总是给出简短的回答”）、对话历史上下文控制、卡片消息渲染（钉钉）、日志服务（SLS）对接等高级功能。

> **注意**：文档 1 中模型名称为 `Qwen3.5-Plus`，而文档 2、3、4 中均写作 `千问-Plus`。根据百炼控制台最新命名规范，`Qwen3.5-Plus` 是当前正式版本名，`千问-Plus` 为旧称或别名，建议以控制台显示为准，避免配置时因名称不一致导致模型加载失败。

## 关键参数

| 参数 | 说明 | 来源位置 |
|------|------|----------|
| `App ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 所有文档（1–4）均要求配置 |
| `API Key` | 百炼 API 调用凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建 | 所有文档（1–4）均要求配置 |
| `AgentKey`（业务空间标识） | 用于鉴权校验，必须确保 AppFlow 连接凭证与百炼应用处于同一业务空间 | 文档 1 的“常见问题”中强调此项 |
| `WebhookUrl` | AppFlow 生成的 HTTP 回调地址，需填入企业微信/钉钉/微信公众号后台 | 文档 3、4、2（认证号流程）均依赖此参数 |
| `Token` & `EncodingAESKey` | 企业微信消息加解密必需参数，由 AppFlow 在创建企业微信凭证时生成 | 文档 3 的 3.3 步骤明确要求保存 |
| `相似度阈值` / `召回片段数` | RAG 检索阶段关键参数，影响知识召回质量与响应长度 | [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 中详细说明 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建**智能体应用** → 选择 `Qwen3.5-Plus` 模型 → 配置 Prompt → 发布。
2. **获取凭证**：在应用管理页复制 `App ID`；在密钥管理页创建并保存 `API Key`。
3. **配置目标渠道**：
   - **网站**：使用 AppFlow 创建 AI 助手 → 导入百炼应用 → Web 页面集成 → 复制悬浮挂件脚本插入 HTML [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
   - **微信公众号**：使用 AppFlow 微信模板 → 授权公众号（区分认证/未认证）→ 绑定百炼应用 → 发布连接流。
   - **企业微信**：创建企业微信自建应用 → 获取 `CorpID`/`AgentId`/`Secret` → AppFlow 模板绑定 → 配置 API 接收消息与可信 IP。
   - **钉钉**：创建钉钉开放平台应用 → 授予卡片权限 → AppFlow 模板绑定 → 配置机器人 HTTP Webhook。
4. **接入私有知识**：上传文件至百炼数据连接 → 创建知识库 → 在应用配置中启用“必定调用”并关联知识库。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、FC、ADB-PG 等依赖云产品单独计费。
- **文件限制**：知识库上传单文件最大 100MB 或 1000 页，支持格式包括 PDF/DOCX/TXT/XLSX/CSV/PNG/JPG 等（文档 3 明确列出）；本地 RAG 方案同样限制单文件 ≤100MB（文档 5）。
- **超时约束**：未认证微信公众号要求响应时间 ≤5 秒，否则无法回复；建议选用 `qwen-turbo` 或优化 Prompt 缩短生成耗时（文档 2 常见问题）。
- **安全校验**：
  - 企业微信要求域名主体备案与企业主体一致，否则需配置自有域名或 Nginx 代理（文档 3）；
  - 微信公众号服务器配置报“URL 存在严重安全风险”时，需改用服务商授权方式（文档 2）；
  - 企业微信可信 IP 冲突时，必须使用 ECS 或托管实例做代理转发（文档 3）。
- **调试要点**：若出现 `request error` 或无响应，优先检查 `App ID`、`API Key`、`AgentKey` 三者是否同属一个业务空间（文档 1 常见问题）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


