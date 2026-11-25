# application [use cases](use-cases.md)

阿里云百炼平台支持将大模型能力快速集成到主流企业协作与客户触点渠道中，包括企业微信、钉钉、微信公众号及自有网站。所有方案均基于无代码/低代码方式（主要依赖 AppFlow 连接流或 Web 集成组件），通过 RAG（[检索增强生成](../concepts/rag.md)）机制接入私有知识，实现 7×24 小时智能问答。核心流程统一为：创建百炼智能体应用 → 配置目标渠道凭证 → 建立连接流或嵌入组件 → 关联知识库 → 发布验证。

## 支持的模型/功能

- **基础模型**：默认推荐 `qwen-plus`（均衡型），部分场景支持 `qwen-max`（高精度）、`qwen3.5-flash`（高吞吐低延迟）及 `qwen3.5-plus`（文档 5 中明确指定）。[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 明确要求使用 `Qwen3.5-Plus`，而其他三篇文档（企业微信、微信公众号、钉钉）均使用 `千问-Plus`（即 `qwen-plus`），需注意版本命名一致性。
- **核心功能**：
  - 智能体（Agent）应用：支持角色设定（Prompt）、多轮对话、[工具调用](../concepts/tool-calling.md)（隐式）；
  - RAG 知识增强：支持上传 `.pdf`, `.docx`, `.txt`, `.md`, `.xlsx`, `.csv` 等格式文件，自动解析并构建向量知识库；
  - 多渠道消息适配：自动处理企业微信/钉钉/公众号/网页的请求格式、签名验证与响应封装；
  - 可视化配置：AppFlow 提供预置模板（如“企业微信自建应用大模型自动回复”），大幅降低集成门槛。

> **注意**：文档 4 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 描述的是**本地部署 RAG 前端 + 调用百炼 API 的混合架构**，与前述 4 篇纯云端 SaaS 集成方案存在本质差异——它要求用户自行维护 Python 环境、管理向量存储（`VectorStore` 目录）、修改源码（如 `chat.py`），不适用于无运维能力的业务方。该方案应视为高级定制选项，而非标准 use case。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **应用标识** | `App ID` | 百炼控制台「应用管理」中生成的唯一 ID，用于连接流调用目标应用 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) §1.2 |
| **认证凭证** | `API Key` | 百炼控制台「密钥管理」生成的密钥，用于 AppFlow 或前端 SDK 鉴权 | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) §1.2 |
| **渠道凭证** | `AgentID` / `Secret`（企微）、`Client ID` / `Client Secret`（钉钉）、`AppID`（公众号） | 各平台开放平台分配的凭证，用于 AppFlow 授权对接 | [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) §2.2 |
| **RAG 控制** | `召回片段数`、`相似度阈值`、`调用方式`（如“必定调用”） | 控制知识检索精度与生成质量，可在知识库配置页或应用设置中调整 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) §5.1 |

## 使用方式

1. **创建智能体应用**：  
   进入百炼控制台「应用管理」→「创建应用」→ 选择「智能体应用」→ 设置模型（`qwen-plus` 或 `Qwen3.5-Plus`）与 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）→ 发布。

2. **配置目标渠道**：  
   - **企业微信/钉钉/公众号**：在对应开放平台创建应用，获取 `AgentID/Secret`、`Client ID/Secret` 或 `AppID`；  
   - **网站**：无需第三方平台凭证，直接在 AppFlow「模型服务AI助手」中创建并配置悬浮挂件。

3. **建立连接流或嵌入组件**：  
   - 企业微信/钉钉/公众号：使用 AppFlow 预置模板（如 `tl-qiyeweixinself0813shzoa`），依次配置渠道凭证、百炼 API Key、应用 ID；  
   - 网站：在 AppFlow「AI助手」→「Web页面集成」中生成悬浮挂件脚本，插入 HTML `<head>` 或 `<body>` 底部。

4. **接入私有知识**：  
   - 上传文件至百炼「数据连接」→ 创建「知识库」→ 在目标智能体应用中启用知识库并设为「必定调用」→ 重新发布应用。

5. **验证与发布**：  
   - 企业微信/钉钉：搜索应用名称或添加机器人至群聊后 `@` 测试；  
   - 公众号：关注后发送消息；  
   - 网站：刷新页面点击右下角悬浮图标。

## 限制和注意事项

- **文件限制**：单文件最大 100 MB 或 1000 页（企业微信/钉钉/公众号方案）；本地 RAG 方案（文档 4）明确提示“不建议传入超过 100 MB 的文件”以避免限流超时。
- **认证依赖**：微信公众号若未完成认证，仅支持被动回复（5 秒内响应），且无法同时启用服务器配置与自定义菜单；已认证公众号可调用客服消息接口实现主动推送。
- **可信 IP 与域名**：企业微信强制校验可信 IP 和域名主体。若使用 AppFlow 默认 Webhook，需配置二级域名（如 `airobot.example.com`）并完成 CNAME 解析；或启用「内网代理」模式，将请求转发至自有 ECS/Nginx 实例，并将其 IP 加入企业微信可信列表。
- **调试排查**：  
  - 若对话无响应，优先检查 AppFlow 执行日志（「运行日志」→「详情」），常见错误包括 `App ID` 前后空格、API Key 失效、渠道凭证未授权；  
  - 网站嵌入报 `request error` 或 `Failed to stream content`，需确认前端脚本是否来自当前 AI 助手实例、API Key 与应用 ID 是否在同一业务空间（`AgentKey` 一致）。
- **日志与分析**：可通过 AppFlow 添加 SLS 日志节点记录完整对话流，用于效果评测与持续优化。

## 来源文档

- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)


