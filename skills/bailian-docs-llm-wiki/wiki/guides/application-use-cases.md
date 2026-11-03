# application [use cases](use-cases.md)

百炼平台支持多种主流企业通讯与内容平台的 AI 助手集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流 + 可选私有知识库实现端到端交付。核心流程高度一致：创建百炼智能体应用 → 配置模型与凭证 → 在目标平台完成身份/消息通道对接 → 可选接入知识库提升专业性。开发者可复用同一套百炼应用和知识库，在不同渠道快速部署一致体验的 AI 助手。

## 支持的模型/功能

- **基础模型**：所有用例默认推荐 `qwen-plus`（即文档中多次提及的“千问-Plus”），该模型在效果、速度与成本间取得平衡；[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 明确指出其“推理效果、成本和速度介于千问Max和千问Flash之间”。  
- **可选模型**：`qwen-max`（高效果）、`qwen3.5-flash`（高速低延迟）、`qwen3.5-plus`（文档 1 中使用，为 qwen-plus 的演进版本）。  
- **核心功能**：  
  - 智能体（Agent）能力：支持多轮对话、工具调用（如知识库检索）；  
  - RAG 增强：通过百炼知识库模块接入私有文档（PDF/DOCX/TXT 等），支持全文引用、切片检索、自定义处理三种文件处理方式；  
  - 多平台消息适配：AppFlow 提供预置模板，自动处理各平台消息格式（如微信公众号的被动回复超时限制、钉钉卡片消息权限配置等）。

> **注意**：文档 1 使用 `Qwen3.5-Plus`，而文档 2、3、5 均使用 `千问-Plus`。根据百炼最新模型命名规范，`qwen-plus` 是当前标准名称，`Qwen3.5-Plus` 属于旧版命名，实际为同一模型。建议开发者统一使用控制台显示的 `qwen-plus` 标识，避免因名称差异导致配置错误。

## 关键参数

| 参数 | 说明 | 典型取值 | 来源依据 |
|------|------|----------|----------|
| `应用ID`（App ID） | 百炼应用唯一标识，在应用管理页获取 | `app-xxxxxx` | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 1.2 节 |
| `API Key` | 百炼服务调用凭证，在密钥管理页创建 | `sk-xxxxxxxx` | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 1.2 节 |
| `AgentKey`（业务空间标识） | 用于鉴权，必须与 API Key 所属业务空间一致 | 控制台自动填充 | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题第 2 条 |
| `WebhookUrl` | AppFlow 连接流对外暴露的 HTTP 回调地址，需填入目标平台（如企业微信、钉钉） | `https://xxx.appflow.aliyuncs.com/xxx` | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 3.3 节 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `qwen-plus`）→ 配置 Prompt（如角色设定）→ 发布。  
2. **获取凭证**：在应用管理页复制 `应用ID`；在密钥管理页创建并保存 `API Key`。  
3. **配置目标平台连接**：  
   - **网站**：使用 AppFlow 创建 AI 助手 → 导入百炼应用 → Web 页面集成 → 获取悬浮挂件脚本并嵌入 HTML。  
   - **微信公众号/企业微信/钉钉**：使用 AppFlow 对应平台模板（如 `tl-qiyeweixinself0813shzoa`）→ 授权平台账号（如企业微信 AgentId/Secret）→ 绑定百炼 API Key 和应用ID → 获取 `WebhookUrl` → 在平台后台配置消息接收地址。  
4. **（可选）接入知识库**：上传文档 → 创建知识库 → 在百炼应用配置中启用“必定调用”并关联知识库 → 重新发布应用。  

> **注意**：文档 3 明确指出，未认证的微信公众号受 5 秒响应限制，若百炼应用响应超时将失败；此时需优化 Prompt（如添加“请总是给出简短的回答”）或切换至更快速模型（如 `qwen3.5-flash`），详见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 常见问题。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；超出后按 token 计费。AppFlow、函数计算（FC）、ADB-PG 等依赖云产品单独计费。  
- **知识库限制**：单文档最大 100MB 或 1000 页；图片单张最大 20MB；最多上传 200 个文件；文档解析耗时约 1–6 分钟。  
- **平台特异性限制**：  
  - 微信公众号未认证时仅支持被动回复（5 秒超时），且无法同时启用自定义菜单；  
  - 企业微信要求配置可信 IP 白名单，若使用第三方代理需启用内网代理并配置 ECS 实例；  
  - 钉钉机器人必须使用 HTTP 模式（非 Stream 模式），否则无法返回消息。  
- **本地 RAG 方案**：文档 4 提供了基于本地知识库的完整 RAG 实现（`local_rag.zip`），适用于需完全掌控数据切分、嵌入模型选择的场景，但需自行维护 Python 环境（3.9–3.12）及依赖。该方案不依赖百炼知识库服务，而是调用百炼 Embedding API 或本地模型生成向量。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


