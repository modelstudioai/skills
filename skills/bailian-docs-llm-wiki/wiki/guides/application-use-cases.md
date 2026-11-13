# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景，所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 无代码连接流实现。核心流程一致：创建百炼智能体应用 → 配置知识库 → 在目标渠道通过 AppFlow 绑定模型与消息入口。开发者可复用同一套知识库和提示词配置，降低多端维护成本。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档 3 提及用于提速），具体选型需结合响应时延与准确率要求权衡。
- **RAG 能力**：所有用例均依赖百炼知识库实现私有知识增强，支持 PDF/DOCX/TXT/XLSX/CSV/PPT 等格式（文档 2 明确列出支持格式），默认采用文档智能解析，支持全文引用、切片检索与自定义处理三种文件处理方式（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。
- **交互能力**：支持 Web 悬浮挂件（文档 1）、微信公众号被动/主动回复（文档 3）、企业微信自建应用消息（文档 2）、钉钉机器人 HTTP 模式卡片（文档 4），以及本地部署的 Gradio Web UI（文档 5）。

> **注意**：文档 1 与文档 2–4 在模型名称表述上存在不一致——文档 1 使用 `Qwen3.5-Plus`，而文档 2、3、4 均简写为 `千问-Plus`。根据百炼控制台最新命名规范，应以 `Qwen3.5-Plus` 为准，`千问-Plus` 为旧版别名，可能指向不同模型版本，建议开发者在控制台实际下拉菜单中确认模型 ID。

## 关键参数

- **应用 ID 与 API Key**：必需参数，用于百炼应用鉴权。API Key 需在百炼控制台 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建，应用 ID 在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面获取（[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。
- **知识库调用方式**：关键行为控制参数，包括 `必定调用`（强制检索）、`按需调用`（模型自主判断）、`不调用`；同时支持为每个知识库设置 `相似度阈值` 和 `权重`（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。
- **RAG 检索参数（仅本地 RAG）**：文档 5 提供细粒度控制，包括 `召回片段数`（控制检索结果数量）、`相似度阈值`（过滤低相关片段）、`温度`、`最大回复长度`、`上下文轮数`等，适用于需深度调优的场景（[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。

## 使用方式

1. **创建百炼智能体应用**：进入百炼控制台 → 应用管理 → 创建智能体应用 → 选择模型（如 `Qwen3.5-Plus`）→ 编辑 Prompt（例如 `"你叫小助，可以帮助用户解答产品选购、使用等方面的问题。"`）→ 发布。
2. **配置知识库**：上传业务文档（PDF/DOCX 等）→ 创建知识库（标准版）→ 在应用配置中启用知识库并设为 `必定调用` → 再次发布。
3. **绑定渠道与消息流**：
   - **网站**：AppFlow 创建 AI 助手 → 导入百炼应用 → Web 页面集成 → 复制悬浮挂件脚本插入 HTML。
   - **微信公众号/企业微信/钉钉**：AppFlow 使用对应模板 → 授权渠道账号（公众号主管理员扫码、企业微信填 AgentId/Secret、钉钉填 Client ID/Secret）→ 绑定百炼 API Key 与应用 ID → 获取 WebhookUrl → 在渠道后台配置接收地址（公众号服务器配置、企业微信 API 接收、钉钉机器人 HTTP 地址）。
4. **验证与日志**：渠道内直接对话测试；如需分析效果，可在 AppFlow 连接流中添加 SLS 日志节点记录对话（[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）。

## 限制和注意事项

- **认证与权限依赖**：企业微信、钉钉、微信公众号均需对应平台的开发者权限或企业认证。未认证公众号仅支持 5 秒内被动回复，超时即失败（文档 3）；钉钉应用需手动开通 `Card.Streaming.Write` 权限（文档 4）；企业微信需配置可信 IP 或通过 Nginx 代理解决主体校验问题（文档 2）。
- **知识库容量与性能**：单文档最大 100MB 或 1000 页（文档 2），但文档 5 明确提示“不建议传入超过 100 MB 的文件”，因 Embedding API 限流可能导致创建失败或超时。
- **前端与网络限制**：网站嵌入时若出现 `Failed to stream content` 错误，常见原因为前端请求地址未替换为实际后端服务地址（文档 1）；企业微信域名校验失败需配置二级域名或 Nginx 代理（文档 2）。
- **本地 RAG 特殊要求**：Python 版本需为 3.9–3.12，依赖 `uvicorn` 启动，Windows 用户需额外安装 `msvc-runtime`（文档 5）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


