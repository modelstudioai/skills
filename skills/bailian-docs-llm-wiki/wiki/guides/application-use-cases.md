# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景下的 AI 应用快速落地，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可基于统一的百炼应用（智能体）底座，通过 AppFlow 连接不同渠道（网站、企业微信、钉钉、微信公众号），或部署本地 RAG 服务，实现面向终端用户的智能问答与客服能力。所有方案均默认复用百炼提供的模型 API、知识库与 Prompt 工程能力。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 中一致采用），该模型在效果、速度与成本间取得平衡，适用于通用客服问答场景；也可按需切换为 `qwen-max`（高精度）、`qwen-turbo`（低延迟）或 `qwen-flash`（文档 1 提及对比）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **核心功能**：
  - 智能体（Agent）编排：支持多步骤任务、工具调用（如知识库检索）；
  - RAG 增强：通过知识库关联文档，实现私域问题精准回答；
  - 多端集成：提供 Web 悬浮窗、企业微信应用、钉钉机器人、微信公众号客服四种开箱即用的渠道接入能力；
  - 本地化 RAG：支持知识库部署在本地，自定义切分、嵌入模型与检索参数 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2–4 统一写作 `千问-Plus`。二者实为同一模型（Qwen3.5-Plus 的中文品牌名），属命名差异，非功能矛盾。

## 关键参数

- **身份凭证**：
  - `App ID`：百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取；
  - `API Key`：用于调用百炼模型 API 的密钥，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面创建；
- **知识库配置**：
  - `调用方式`：关键开关，如 `必定调用`（强制启用 RAG）或 `按需调用`；
  - `相似度阈值` 与 `召回片段数`：直接影响检索质量，可在应用配置页或本地 RAG 应用中调整 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)；
- **Prompt 工程**：
  - 角色设定（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题`）为必填项，直接影响模型行为；
  - 可添加约束（如 `请总是给出简短的回答，不要讲太多`）以适配渠道特性（如微信公众号消息长度限制）。

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt → 发布；
2. **准备知识库（可选但推荐）**：
   - 上传文档（PDF/DOCX/TXT 等）至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)；
   - 在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建并关联文档；
   - 在应用配置中启用知识库，设置调用方式；
3. **选择集成渠道并配置 AppFlow**：
   - **网站**：AppFlow → 模型服务 AI 助手 → 创建助手 → 导入百炼应用 → Web 页面集成 → 获取悬浮挂件脚本并嵌入 HTML；
   - **企业微信/钉钉/微信公众号**：AppFlow → 使用对应预置模板（如 `企业微信自建应用大模型自动回复`）→ 授权第三方平台凭证（企业 ID/AgentId/Secret 或 AppID）→ 关联百炼应用 → 获取 Webhook URL 并配置到对应平台后台；
4. **验证与日志**：在目标渠道发起对话测试；如需分析效果，可在 AppFlow 连接流中添加 SLS 日志节点记录对话 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；额度用尽后按 token 计费；AppFlow、函数计算 FC、ADB-PG 等依赖云产品单独计费；
- **认证要求**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口；
  - 企业微信/钉钉应用需由具备开发者权限的账号创建；
- **安全与合规**：
  - 企业微信要求配置可信 IP 白名单，若使用 AppFlow 默认出口 IP 冲突，需启用内网代理（ECS/Nginx）；
  - 微信公众号配置服务器地址时若报“安全风险”，需改用服务商授权模式重新创建连接流；
- **技术限制**：
  - 本地 RAG 方案中，单文件上传建议 ≤100 MB，避免 Embedding API 限流导致创建失败；
  - 钉钉机器人仅支持 HTTP 模式接收消息，Stream 模式不可用；
  - 所有渠道均依赖百炼应用已发布（未发布的应用无法被外部调用）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


