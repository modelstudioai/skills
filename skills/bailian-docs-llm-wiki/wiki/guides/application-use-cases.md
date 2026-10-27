# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG 架构，通过百炼大模型应用 + AppFlow 无代码连接流实现端到端交付，开发者只需配置模型、凭证和知识库，无需编写后端逻辑。核心能力包括私有知识注入、多轮对话管理、跨平台消息协议适配及日志可观测性。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）、`千问-Plus`（文档 2、3、4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（极致响应速度）[原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **RAG 增强**：所有用例均支持知识库配置，可上传 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.pptx`, `.png`, `.jpg` 等格式文件（文档 2、3、4、5），最大单文件 100 MB（文档 2、5）。
- **本地部署选项**：除云端标准 RAG 外，还提供基于本地知识库的完整 RAG 应用框架，支持自定义文档切分、本地 embedding 模型（如 `nlp_gte_sentence-embedding_chinese-large`）及 Gradio Web UI [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **扩展能力**：支持对话日志写入 SLS（文档 2、3、4）、AI 卡片消息（钉钉）、流式响应（文档 1）、DeepSeek 思考过程展示（文档 4）等高级功能。

> **注意**：文档 1 中明确推荐 `Qwen3.5-Plus`，而文档 2、3、4 统一使用 `千问-Plus`。经核实，`千问-Plus` 是 `Qwen3.5-Plus` 的旧称，二者为同一模型，当前控制台已统一显示为 `Qwen3.5-Plus`。请以百炼控制台实际模型列表为准。

## 关键参数

| 参数 | 说明 | 取值建议 | 来源 |
|------|------|----------|------|
| `应用ID` | 百炼应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面获取 | 必填，不可为空格 | 文档 1、2、3、4 |
| `API Key` | 百炼调用凭证，在[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建 | 必填，需与应用同业务空间 | 文档 1、2、3、4 |
| `AgentKey` / `业务空间标识` | 用于鉴权校验，确保 API Key 与智能体归属同一业务空间 | 必须一致，否则报 `request error` | [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| `知识库调用方式` | 控制知识检索触发策略 | `必定调用`（强依赖私有知识）、`按需调用`（默认） | 文档 1、2、3、4 |
| `相似度阈值` | 过滤低相关性召回片段 | 默认 0（不过滤），建议 0.3–0.7 范围内调优 | 文档 5 |
| `召回片段数` | 检索返回给大模型的文本段数量 | 默认 3，可设为 1–5；值过高易引入噪声 | 文档 5 |

## 使用方式

1. **创建百炼应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 配置 Prompt（如角色设定）→ 发布。
2. **准备知识库（可选但推荐）**：上传文档 → 创建知识库 → 在应用配置中启用并关联知识库 → 设置调用方式与阈值。
3. **配置连接流**：
   - 网站：使用 AppFlow 创建 AI 助手 → 导入百炼模型 → 配置 Web 集成 → 获取悬浮挂件脚本 → 插入 HTML。
   - 微信公众号/企业微信/钉钉：使用对应 AppFlow 模板 → 授权平台凭证（AppID/AgentId/Client ID + Secret）→ 关联百炼应用 → 获取 Webhook URL。
4. **平台侧配置**：
   - 公众号：后台开启服务器配置，填写 Webhook URL、Token、EncodingAESKey。
   - 企业微信：配置 API 接收消息 + 可信 IP 白名单（需注意可信 IP 冲突问题）。
   - 钉钉：配置机器人 HTTP 模式接收地址 → 发布应用版本 → 群内添加机器人。
5. **验证与日志**：发起测试对话；如失败，通过 AppFlow 运行日志排查（文档 3）；可选添加 SLS 日志节点记录全链路对话 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 限制和注意事项

- **免费额度**：新用户可享百炼免费额度，覆盖教程全部调用消耗；额度用尽后按 token 计费（文档 1、2、4）。
- **认证要求**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客服接口（文档 3）。
  - 企业微信需配置自有域名或 Nginx 代理解决“域名主体校验未通过”问题（文档 2）。
- **安全限制**：
  - 企业微信要求可信 IP 为本企业服务器 IP，第三方 IP（如 AppFlow 默认出口）将被拒绝（文档 2）。
  - 钉钉机器人必须使用 **HTTP 模式**，Stream 模式不兼容（文档 4）。
- **技术约束**：
  - 本地 RAG 应用要求 Python 3.9–3.12，Windows 用户需额外安装 `msvc-runtime`（文档 5）。
  - 知识库文件解析耗时 1–6 分钟，大文件（>100 MB）可能导致创建失败（文档 2、5）。
- **调试要点**：常见 `request error` 原因包括 API Key 失效、`AgentKey` 不匹配、应用 ID 错误或含空格（文档 1）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


